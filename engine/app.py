from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)

CORS(app)

rooms = [
        {"id": 1, "name": "Living Room"},
        {"id": 2, "name": "Kitchen"},
        {"id": 3, "name": "Bedroom"},
        {"id": 4, "name": "Bathroom"}
    ]

devices = [
        {"id": 1, "type" : "Light", "roomId" : 1},
        {"id": 2, "type" : "Thermometer", "roomId" : 1},
        {"id": 3, "type" : "Alarm", "roomId" : 1},
        {"id": 4, "type" : "Light", "roomId" : 2},
        {"id": 5, "type" : "Light", "roomId" : 3},
        {"id": 6, "type" : "Light", "roomId" : 4}
    ]

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
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

@app.route('/api/rooms/add', methods=['POST'])
def add_room():
    data = request.get_json()
    
    #TODO: Lepse ovo validirati, da li postoji itd.
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'Room name is required'}), 400

    new_room = {
        'id': str(uuid.uuid4()),
        'name': data['name']
    }

    rooms.append(new_room)
    return jsonify(new_room), 201

@app.route('/api/rooms/remove/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    global rooms
    rooms = [r for r in rooms if r['id'] != room_id]
    return jsonify({'message': 'Room deleted successfully'}), 200






if __name__ == '__main__':
    app.run(debug = True, port = 8000)
