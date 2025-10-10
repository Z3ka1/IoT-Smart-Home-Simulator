from machine import Pin
import network
import urequests as requests
import ujson as json
import RGB1602
import time
import math

#WIFI connection
SSID = ""
PASSWORD = ""

def try_connect(ssid, password):
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

def get_new_credentials():
    print("Enter new WiFi credentials:")
    ssid = input("SSID: ")
    password = input("Password: ")
    
    if try_connect(ssid, password):
        with open('wifi_creds.txt', 'w') as f:
            f.write(ssid + '\n')
            f.write(password + '\n')
        print("New credentials saved successfuly!")
        return True
    else:
        print("Failed to connect with new credentials.")
        return False

def connect_wifi():
    try:
        with open('wifi_creds.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                ssid = lines[0].strip()
                password = lines[1].strip()
                print(f"Found saved credentials for: {ssid}")
                
                if try_connect(ssid, password):
                    return True
    except:
        print("No saved credentials found or file error")
        
    return get_new_credentials()


#Device implementation
DEVICE_TYPE = "lcddisplay"
BACKEND_URL = "http://192.168.0.41:8000"

device_id = None

def save_device_id(device_id):
    with open("device_id.txt", "w") as f:
        f.write(str(device_id))
        
def load_device_id():
    try:
        with open("device_id.txt", "r") as f:
            return f.read().strip()
    except OSError:
        return None

def pair_device():
    global device_id
    print("Pairing started...")
    payload = {
        "type": DEVICE_TYPE,
        "properties": {
            "state": "off",
            "first_line_text": "",
            "second_line_text": "",
            "display_theme": "matrix-green"
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


themes = { "matrix-green": [0, 128, 60],
           "purple-haze": [148, 0, 110],
           "lime-burst": [144, 249, 15],
           "amber-glow": [255, 209, 0],
           "solar-flare": [248, 248, 60],
           "midnight-blue": [80, 80, 145],
           "crimson": [255, 0, 0],
           "electric-lime": [0, 255, 0]
        }

POLL_TIME = 2

colorR = 0
colorG = 128
colorB = 60

lcd=RGB1602.RGB1602(16,2)
#lcd.clear()
#lcd.setRGB(0,0,0)

first_line_text = ""
second_line_text = ""
current_state = "off"
display_theme = "matrix-green"
change_detected = False

def poll_properties():
    global first_line_text
    global second_line_text
    global current_state
    global display_theme
    global colorR
    global colorG
    global colorB
    global change_detected
    try:
        res = requests.get(f"{BACKEND_URL}/api/devices/lcddisplay/{device_id}/poll_properties")
        if res.status_code == 200:
            props = res.json().get("properties", {})
            new_first_line_text = props.get("first_line_text")
            new_second_line_text = props.get("second_line_text")
            new_state = props.get("state")
            new_theme = props.get("display_theme")
            
            if new_first_line_text != first_line_text or new_second_line_text != second_line_text or new_state != current_state or new_theme != display_theme:
                print("Properties changed: ", props)
                current_state = new_state
                first_line_text = new_first_line_text
                second_line_text = new_second_line_text
                display_theme = new_theme
                colorR, colorG, colorB = themes[display_theme]
                change_detected = True
        else:
            print("Failed to fetch state: ", res.status_code)
        res.close() # Memory must be cleared
    except Exception as e:
        print("Polling error: ",e)



if SSID != "" and PASSWORD != "":
    try_connect(SSID, PASSWORD)
else:
    connect_wifi()
print("\n\n")

device_id = load_device_id()
print(f"device_id = {device_id}")
if device_id == None:
    input("Press Enter to pair this device")
    pair_device()

while True:
    poll_properties()
    if current_state and change_detected:
        lcd.clear()
        lcd.setRGB(colorR, colorG, colorB)
        lcd.setCursor(0, 0)
        lcd.printout(first_line_text)
        lcd.setCursor(0, 1)
        lcd.printout(second_line_text)
        
        change_detected = False
    elif not current_state:
        lcd.setRGB(0, 0, 0)
    time.sleep(POLL_TIME)

