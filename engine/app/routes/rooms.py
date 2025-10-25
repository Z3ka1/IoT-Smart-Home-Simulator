from flask import Blueprint, jsonify, request
from app.models.room import Room
from app.models.gateway import Gateway
from app.models.device import Device
from app import db
from ..utils.jwt_utils import token_required

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
@token_required
def get_rooms():
    gateway_id = request.gateway_id

    gateway = Gateway.query.get(gateway_id)
    if not gateway:
        return jsonify({'error': 'Invalid gateway'}), 401

    rooms = Room.query.filter_by(gateway_id = gateway_id).all()
    return jsonify([{"id": r.id, "gateway_id": r.gateway_id, "name": r.name} for r in rooms])

@rooms_bp.route('/rooms', methods=['POST'])
@token_required
def add_room():
    data = request.get_json()
    gateway_id = request.gateway_id
 
    room_name = data.get('name', '').strip()
    if not room_name:
        return jsonify({"error": "Room name is required"}), 400
    
    existing_room = Room.query.filter_by(name = room_name, gateway_id = gateway_id).first()
    if existing_room:
        return jsonify({"error": f"Room '{room_name}' already exists."}), 400

    new_room = Room(name=data['name'], gateway_id = gateway_id)
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"id": new_room.id, "name": new_room.name, "gateway_id": new_room.gateway_id}), 201

@rooms_bp.route('/rooms/remove/<room_id>', methods=['DELETE'])
@token_required
def delete_room(room_id):
    gateway_id = request.gateway_id
    room = Room.query.filter_by(id = room_id, gateway_id = gateway_id).first()
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted successfully'}), 200

@rooms_bp.route('/rooms/<room_id>/devices', methods=['GET'])
@token_required
def get_devices_in_room(room_id):
    gateway_id = request.gateway_id
    devices = Device.query.filter_by(room_id=room_id, gateway_id=gateway_id).all()
    return jsonify({
        "devices": [
            {"id": d.id, "name": d.name, "type": d.type}
            for d in devices
        ]
    }), 200

@rooms_bp.route('/rooms/device-counts', methods=['GET'])
@token_required
def get_room_device_counts():
    gateway_id = request.gateway_id
    
    # Query to count devices per room
    room_counts = db.session.query(
        Room.id, 
        Room.name,
        db.func.count(Device.id).label('device_count')
    ).outerjoin(Device, Room.id == Device.room_id)\
     .filter(Room.gateway_id == gateway_id)\
     .group_by(Room.id, Room.name)\
     .all()
    
    # Convert to dictionary format
    counts_dict = {
        room.id: {
            'name': room.name,
            'device_count': room.device_count
        }
        for room in room_counts
    }
    
    return jsonify(counts_dict), 200