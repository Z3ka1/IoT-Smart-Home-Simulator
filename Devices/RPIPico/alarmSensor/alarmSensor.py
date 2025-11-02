from NETWORKING import try_connect, get_new_credentials, connect_wifi, discover_with_retry, save_device_id, load_device_id
import machine
import network
import time
import utime
import urequests as requests
import ujson as json

#WIFI connection
SSID = ""
PASSWORD = ""

#Device implementation
DEVICE_TYPE = "alarmSensor"
device_id = None

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
                #print("Is alarm enabled = ", new_state)
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

server_ip, server_port = discover_with_retry()
BACKEND_URL = f'http://{server_ip}:{server_port}'
print("\n")

device_id = load_device_id()
print(f"device_id = {device_id}")
if device_id == None and server_port != None:
    input("Press Enter to start pairing.")
    pair_device()

if server_port != None:
    sensor_pir.irq(trigger = machine.Pin.IRQ_RISING, handler = pir_handler)

    last_poll = utime.ticks_ms()
    alarm_end = 0
    is_motion_detection_event_sent = False

    try:
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
    except KeyboardInterrupt:
        print("Device turning off...")
        buzzer.value(0)
        led.value(0)
else:
    print("Server can't be discovered. Alarm is turning off...")