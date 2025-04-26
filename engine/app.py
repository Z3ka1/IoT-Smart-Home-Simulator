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
        {"id": 1, "type" : "Light", "roomId" : 1},
        {"id": 2, "type" : "Thermometer", "roomId" : 1},
        {"id": 3, "type" : "Alarm", "roomId" : 1},
        {"id": 4, "type" : "Light", "roomId" : 2},
        {"id": 5, "type" : "Light", "roomId" : 3},
        {"id": 6, "type" : "Light", "roomId" : 4}
    ]
    return jsonify(devices), 200

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
