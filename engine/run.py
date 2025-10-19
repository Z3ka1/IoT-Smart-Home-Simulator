from app import create_app, socketio
import socket
import threading
import os

app = create_app()

def start_discovery_server(port = 50000):

    # If in DEBUG mode we need to make sure only one listener is created on port
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        print("[DISCOVERY] Skipping in reloader process")
        return

    def discovery_responder(port = 50000, flask_port = 8000):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", port))

        print(f"[DISCOVERY] Listening for discovery on UDP {port}")

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.decode().strip() == 'SMART_HOME_SERVER_DISCOVERY':
                    print(f"[DISCOVERY] Request from {addr[0]}")
                    # Send response with server info
                    response = f"SMART_HOME_SERVER:{flask_port}"
                    sock.sendto(response.encode(), (addr[0], port+1))
            except Exception as e:
                print(f"[DISCOVERY] Error: {e}")
                
    thread = threading.Thread(target=discovery_responder, daemon= True, name="discovery_responder")
    thread.start()

@app.route('/emit-status', methods=['POST'])
def emit_status():
    from flask import request, jsonify
    try:
        data = request.get_json()
        socketio.emit('device_status', {
            'id': data['id'],
            'available': data['available']
        }, namespace='/')
        
        # Return the number of active clients
        active_clients = len(socketio.server.manager.rooms.get('/', []))
        return jsonify({
            'status': 'success',
            'active_clients': active_clients
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/emit-motion_detected', methods=['POST'])
def emit_motion_detected():
    from flask import request, jsonify
    try:
        data = request.get_json()
        socketio.emit('motion_detected', {
            'id': data['id'],
            'motion_detected': data['motion_detected']
        }, namespace='/')

        active_clients = len(socketio.server.manager.rooms.get('/', []))
        return jsonify({
            'status': 'success',
            'active_clients': active_clients
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/emit-weather_station_measurements', methods=['POST'])
def emit_weather_station_measurements():
    from flask import request, jsonify
    try:
        data = request.get_json()
        socketio.emit('weather_station_measurements', {
            'id': data['id'],
            'temperature': data['temperature'],
            'humidity': data['humidity'],
            'city': data['city'],
            'api_temperature': data['api_temperature'],
            'api_weather_description': data['api_weather_description'],
            'api_feels_like': data['api_feels_like'],
            'api_pressure': data['api_pressure'],
            'api_humidity': data['api_humidity'],
            'last_measurement': data['last_measurement']
        }, namespace='/')

        active_clients = len(socketio.server.manager.rooms.get('/', []))
        return jsonify({
            'status': 'success',
            'active_clients': active_clients
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    start_discovery_server(port = 50000)

    socketio.run(app, debug=True, host="0.0.0.0", port = 8000)