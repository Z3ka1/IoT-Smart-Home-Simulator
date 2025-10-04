import machine
import network
import time
import utime
import urequests as requests
import ujson as json

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
DEVICE_TYPE = "alarmSensor"
BACKEND_URL = "http://192.168.0.27:8000"

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
            "motion_detected": False,
            "is_alarm_enabled": False
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
        
        
# this tells if alarm is turned on
is_alarm_enabled = False
def poll_alarm_enabled():
    global is_alarm_enabled
    try:
        res = requests.get(f"{BACKEND_URL}/api/devices/alarmsensor/{device_id}/alarm_enabled")
        if res.status_code == 200:
            props = res.json().get("properties", {})
            new_state = props.get("is_alarm_enabled")
            
            if new_state != is_alarm_enabled:
                print("Is alarm enabled = ", new_state)
                is_alarm_enabled = new_state
        else:
            print("Failed to fetch is_alarm_enabled: ", res.status_code)
        res.close() # Memory must be cleared
    except Exception as e:
        print("Polling error: ",e)
        
def send_motion_detected_event(event):
    try:
        payload = {
            "properties": {
                "motion_detected": event
            }
        }
        headers = {"Content-Type": "application/json"}
        res = requests.put(f"{BACKEND_URL}/api/devices/alarmsensor/{device_id}/motion_detected",
                           data = json.dumps(payload),
                           headers = headers)
        if res.status_code != 200:
            print("failed to send motion detected event:" ,res.text)
        res.close()
    except  Exception as e:
        print("Error sending motion event:", e)
        
        
sensor_pir = machine.Pin(28, machine.Pin.IN)
led = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.Pin(14, machine.Pin.OUT)

motion_detected = False
def pir_handler(pin):
    global motion_detected
    global is_alarm_enabled
    if is_alarm_enabled:
        motion_detected = True
 
 
POLL_TIME = 2 # in seconds
ALARM_DURATION = 2 # in seconds
 
# Main
if SSID != "" and PASSWORD != "":
    try_connect(SSID, PASSWORD)
else:
    connect_wifi()
print("\n")

device_id = load_device_id()
print(f"device_id = {device_id}")
if device_id == None:
    input("Press Enter to start pairing.")
    pair_device()

sensor_pir.irq(trigger = machine.Pin.IRQ_RISING, handler = pir_handler)

last_poll = utime.ticks_ms()
alarm_end = 0
is_motion_detection_event_sent = False
while True:
    if utime.ticks_diff(utime.ticks_ms(), last_poll) > (POLL_TIME * 1000):
        poll_alarm_enabled()
        last_poll = utime.ticks_ms()
    
    if is_alarm_enabled:
        led.toggle()
        utime.sleep(0.2)
    else:
        led.value(0)
        
    if motion_detected and is_alarm_enabled:
        print("ALARM! Motion detected!")
        alarm_end = utime.ticks_add(utime.ticks_ms(), ALARM_DURATION * 1000)
        send_motion_detected_event(True)
        is_motion_detection_event_sent = True
        motion_detected = False
        
    if utime.ticks_diff(alarm_end, utime.ticks_ms()) > 0:
        buzzer.toggle()
        #led.toggle()
        utime.sleep_ms(100)
    else:
        buzzer.value(0)
        if is_motion_detection_event_sent:
            send_motion_detected_event(False)
            is_motion_detection_event_sent = False
            