import network
import urequests as requests
import ujson as json
import time
import socket

# WiFi connection
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

# Flask Server IP discovery
def discover_server(port = 50000):
    #print("Starting server discovery...")
    
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.settimeout(5)
    recv_sock.bind(('0.0.0.0', port+1))
    
    try:
        broadcast_addr = ('255.255.255.255', port)
        send_sock.sendto(b'SMART_HOME_SERVER_DISCOVERY', broadcast_addr)
        #print("Discovery request sent...")
        
        #print("Waiting for server response...")
        data, addr = recv_sock.recvfrom(1024)
        response = data.decode().strip()
        #print(f"Received response: {response}")
        
        if response.startswith('SMART_HOME_SERVER:'):
            server_port = int(response.split(':')[1])
            print(f"[DISCOVERY] Server found at {addr[0]}:{server_port}")
            return addr[0], server_port
    
    except Exception as e:
        print(f"[DISCOVERY] Failed {e}")
    finally:
        send_sock.close()
        recv_sock.close()
        
    return None, None

def discover_with_retry(port = 50000, max_attempts=3):
    for attempt in range(max_attempts):
        print(f"[DISCOVERY] Attempt {attempt + 1}/{max_attempts}")
        server_ip, server_port = discover_server(port)
        
        if server_ip:
            return server_ip, server_port
        
        if attempt < max_attempts - 1:
            print("[DISCOVERY] Retrying in 3 seconds...")
            time.sleep(3)
    
    return None, None

# Device ID manipulation
def save_device_id(device_id):
    with open("device_id.txt", "w") as f:
        f.write(str(device_id))
        
def load_device_id():
    try:
        with open("device_id.txt", "r") as f:
            return f.read().strip()
    except OSError:
        return None
