from NETWORKING import try_connect, get_new_credentials, connect_wifi, discover_server, save_device_id, load_device_id
from ws2812b import WS2812
import time
import network
import urequests as requests
import ujson as json

#WIFI connection
SSID = ""
PASSWORD = ""

#Device implementation
DEVICE_TYPE = "rgbstrip"
POLL_TIME = 2 #In seconds, how often device pols for new data

device_id = None

NUM_LEDS = 8
LED_PIN = 0
INITIAL_BRIGHTNESS = 0.1

red = 0
green = 0
blue = 0
brightness = 0.1
current_state = "off"

def pair_device():
    global device_id
    print("Pairing started...")
    payload = {
        "type": DEVICE_TYPE,
        "properties": {
            "state": "off",
            "red": 0,
            "green": 0,
            "blue": 0,
            "brightness": 0.1
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
        
def poll_properties():
    global red
    global green
    global blue
    global brightness
    global current_state
    try:
        res = requests.get(f"{BACKEND_URL}/api/devices/rgbstrip/{device_id}/poll_properties")
        if res.status_code == 200:
            props = res.json().get("properties", {})
            new_red = props.get("red")
            new_green = props.get("green")
            new_blue = props.get("blue")
            new_brightness = props.get("brightness")    # / 100 TODO
            new_state = props.get("state")
            
            if new_red != red or new_green != green or new_blue != blue or new_brightness != brightness or new_state != current_state:
                print("Properties changed: ", props)
                current_state = new_state
                red = new_red
                green = new_green
                blue = new_blue
                brightness = new_brightness
        else:
            print("Failed to fetch state: ", res.status_code)
        res.close() # Memory must be cleared
    except Exception as e:
        print("Polling error: ",e)
        

strip = WS2812(LED_PIN, NUM_LEDS, INITIAL_BRIGHTNESS)

strip.clear()
strip.show()


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
    
try:
    while True:
        poll_properties()
        if current_state == "on":
            strip.set_brightness(brightness)
            strip.fill((red, green, blue))
        else:
            strip.clear()
        strip.show()
        time.sleep(POLL_TIME)
except KeyboardInterrupt:
    print("RGB Strip is turning off...")
    strip.clear()
    strip.show()
