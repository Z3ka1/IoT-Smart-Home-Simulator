from NETWORKING import try_connect, get_new_credentials, connect_wifi, discover_server, save_device_id, load_device_id
from machine import Pin
import network
import time
import urequests as requests
import ujson as json

#WIFI connection
SSID = ""
PASSWORD = ""

#Device implementation
DEVICE_TYPE = "simpleled"
POLL_TIME = 2 #In seconds, how often device pols for new data

device_id = None
current_state = None

led = Pin(15, Pin.OUT)

def pair_device():
    global device_id
    print("Pairing started...")
    payload = {
        "type": DEVICE_TYPE,
        "properties": {
            "state": "off"
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
    
    
def poll_state():
    global current_state
    try:
        res = requests.get(f"{BACKEND_URL}/api/devices/simpleled/{device_id}/state")
        if res.status_code == 200:
            props = res.json().get("properties", {})
            new_state = props.get("state")
            
            if new_state != current_state:
                print("State changed: ", new_state)
                current_state = new_state
        else:
            print("Failed to fetch state: ", res.status_code)
        res.close() # Memory must be cleared
    except Exception as e:
        print("Polling error: ",e)


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
        poll_state()
        if current_state == "on":
            led.value(1)
        else:
            led.value(0)
        time.sleep(POLL_TIME)
except KeyboardInterrupt:
    print("Turning LED off...")
    led.value(0)