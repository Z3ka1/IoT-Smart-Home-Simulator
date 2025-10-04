import os

def save_device_id(device_id):
    with open("device_id.txt", "w") as f:
        f.write(str(device_id))
        
def load_device_id():
    try:
        with open("device_id.txt", "r") as f:
            return f.read().strip()
    except OSError:
        return None

print(os.listdir())
while True:
    print("\n--- Options ---")
    print("1. Save ID for device")
    print("2. Remove device_id.txt")
    print("3. Print current ID saved")
    print("4. Exit")
    
    choice = input("Enter option: ")
    print()
    
    if choice == '1':
        id = input("Enter device id: ")
        save_device_id(id)
    elif choice == '2':
        if "device_id.txt" in os.listdir():
            os.remove("device_id.txt")
    elif choice == '3':
        print(load_device_id())
    elif choice == '4':
        print("Exiting...")
        break;