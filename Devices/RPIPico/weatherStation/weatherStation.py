from NETWORKING import try_connect, get_new_credentials, connect_wifi, discover_server, save_device_id, load_device_id
from machine import Pin
from machine import Timer
import network
import time
import urequests as requests
import ujson as json
from dht import DHT11
import secrets

#WIFI connection
SSID = ""
PASSWORD = ""

#Device implementation
DEVICE_TYPE = "weatherstation"
POLL_TIME = 2 #In seconds, how often device pols for new data
MEASUREMENT_TIME = 60	# In seconds, how often device measures and sends data

device_id = None

sensor = DHT11(16, Pin.OUT, Pin.PULL_DOWN)
temperature = 0
humidity = 0

# Default location
city = "Novi Sad"
latitude = 45.25
longitude = 19.8362

# API Weather
api_temperature = 0
api_weather_description = ""
api_feels_like = 0
api_pressure = 0
api_humidity = 0

def pair_device():
    global device_id
    print("Pairing started...")
    payload = {
        "type": DEVICE_TYPE,
        "properties": {
            "temperature": 0.0,
            "humidity": 0.0,
            "last_measurement": "", # Needs to be set on backend and converted to str.
            "city": "Novi Sad",
            "api_temperature": 0.0,
            "api_weather_description": "",
            "api_feels_like": 0.0,
            "api_pressure": 0.0,
            "api_humidity": 0.0
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/pair-device", data=json.dumps(payload), headers=headers)
        if response.status_code == 201:
            result = response.json()
            device_id = result.get("device_id")
            print("Device registered with ID:", device_id)
            save_device_id(device_id)
        else:
            print("Device registration failed: ", response.text)
        response.close() # Free memory
    except Exception as e:
        print("Error during device registration: ", e)
        
def send_measurements():
    global temperature, humidity
    global city, api_temperature, api_weather_description, api_feels_like, api_pressure, api_humidity
    try:
        payload = {
            "properties": {
                "temperature": temperature,
                "humidity": humidity,
                "city": city,
                "api_temperature": api_temperature,
                "api_weather_description": api_weather_description,
                "api_feels_like": api_feels_like,
                "api_pressure": api_pressure,
                "api_humidity": api_humidity
            }
        }
        headers = {"Content-Type": "application/json"}
        res = requests.put(f"{BACKEND_URL}/api/devices/weatherstation/{device_id}/measurements",
                           data = json.dumps(payload),
                           headers = headers)
        if res.status_code != 200:
            print("Failed to send measurements: " ,res.text)
        res.close()
    except  Exception as e:
        print("Error sending measurements: ", e)

def get_geolocation():
    global latitude, longitude, city
    try:
        response = requests.get('http://ip-api.com/json/').json()
        if response['status'] == 'success':
            latitude = response['lat']
            longitude = response['lon']
            city = response['city']
        response.close()
    except Exception as e:
        print("Error: Can't get geolocation data: ", e)

def get_current_weather_data():
    global latitude, longitude
    global api_temperature, api_weather_description, api_feels_like, api_pressure, api_humidity
    try:
        current_weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather/?lat={latitude}&lon={longitude}&appid={secrets.apiKey}&units=metric").json()
        
        if current_weather['cod'] == 200:
            api_temperature = current_weather['main']['temp']
            api_weather_description = current_weather['weather']['main']
            api_feels_like = current_weather['main']['feels_like']
            api_pressure = current_weather['main']['pressure']
            api_humidity = current_weather['main']['humidity']
        current_weather.close()
    except Exception as e:
        print("Error: Can't get current weather data: ", e)
        
# NOT USED CURRENTLY
def get_forecast_weather_data():
    global latitude, longitude
    try:
        forecast_weather = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={secrets.apiKey}&units=metric").json()
        # TODO
        
        forecast_weather.close()
    except Exception as e:
        print("Error: Can't get forecast weather data: ", e)
        
def ping_server(Source):
    try:
        response = requests.get(f"{BACKEND_URL}/api/devices/{device_id}/ping")
        response.close()
    except Exception as e:
        print("Error: Can't ping server: ", e)
        

# MAIN  
if SSID != "" and PASSWORD != "":
    try_connect(SSID, PASSWORD)
else:
    connect_wifi()
    
server_ip, server_port = discover_server()
BACKEND_URL = f'http://{server_ip}:{server_port}'
print("\n\n")

device_id = load_device_id()
print(f"device_id = {device_id}")
if device_id == None:
    input("Press Enter to pair this device")
    pair_device()
    
    
# TIMER za MERENJA NA SVAKI MINUT UMESTO WHILE TRUE ??

pingTimer = Timer(period = 2000, mode = Timer.PERIODIC, callback = ping_server)

get_geolocation()
try:
    while True:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        print("\r", "Temp = ", temperature, chr(176)+'C ',"Humidity = ", humidity, '%', end = '')
        
        get_current_weather_data()
        send_measurements()
            
        time.sleep(MEASUREMENT_TIME)
except KeyboardInterrupt:
    print("Station is turning off...")
    pingTimer.deinit()