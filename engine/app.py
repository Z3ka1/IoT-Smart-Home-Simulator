from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = [
        {"id": 1, "name": "Living Room"},
        {"id": 2, "name": "Kitchen"},
        {"id": 3, "name": "Bedroom"},
        {"id": 4, "name": "Bathroom"}
    ]
    return jsonify(rooms), 200

@app.route('/api/devices', methods=['GET'])
def get_devices():
    devices = [
        {"id": 1, "name" : "Light", "roomId" : 1},
        {"id": 2, "name" : "Thermometer", "roomId" : 1},
        {"id": 3, "name" : "Alarm", "roomId" : 1},
        {"id": 4, "name" : "Light", "roomId" : 2},
        {"id": 5, "name" : "Light", "roomId" : 3},
        {"id": 6, "name" : "Light", "roomId" : 4}
    ]
    return jsonify(devices), 200

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
