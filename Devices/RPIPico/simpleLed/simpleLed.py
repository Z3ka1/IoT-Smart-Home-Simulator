from machine import Pin
import network
import time
import urequests as requests
import ujson as json

#WIFI connection
SSID = ""
PASSWORD = ""

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print("Connecting to WiFi", end="")
    timeout = 10
    start = time.time()
    while not wlan.isconnected():
        print(".", end = "")
        if time.time() - start > timeout:
            print("\nConnection timed out.")
            return False
        time.sleep(1)
    
    print("\nConnected. IP address:", wlan.ifconfig()[0])
    return True


#
DEVICE_TYPE = "simpleled"
BACKEND_URL = "http://192.168.0.27:8000"
POLL_TIME = 2 #In seconds, how often device pols for new data

# TODO : Ova polja mozda ucitati iz nekog fajla ako je vec ranije dobio id i sl.
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
        else:
            print("Device registration failed: ", response.text)
        response.close() # Free memory
    except Exception as e:
        print("Error during device registration: ", e)
    
    
def poll_state():
    global current_state
    while True:
        try:
            res = requests.get(f"{BACKEND_URL}/api/devices/simpleled/{device_id}/state")
            if res.status_code == 200:
                props = res.json().get("properties", {})
                print("props: ")
                print(res.json().get("properties"))
                print("PRISTIGLO")
                print(props.get("state"))
                new_state = props.get("state")
                
                if new_state != current_state:
                    print("State changed: ", new_state)
                    if new_state == "on":
                        led.value(1)
                    else:
                        led.value(0)
                    current_state = new_state
            else:
                print("Failed to fetch state: ", res.status_code)
            res.close() # Memory must be cleared
        except Exception as e:
            print("Polling error: ",e)
            
        time.sleep(POLL_TIME)


print("Start")
connect_wifi(SSID, PASSWORD)
print("Finish\n\n")

if device_id == None:
    input("Press Enter to pair this device")
    pair_device()

poll_state()