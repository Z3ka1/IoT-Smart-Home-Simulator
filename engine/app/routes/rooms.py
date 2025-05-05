from flask import Blueprint, jsonify, request
from app.models.room import Room
from app import db

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{"id": r.id, "gateway_id": r.gateway_id, "name": r.name} for r in rooms])

@rooms_bp.route('/rooms', methods=['POST'])
def add_room():
    data = request.get_json()
    new_room = Room(name=data['name'])
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"id": new_room.id, "name": new_room.name}), 201

@rooms_bp.route('/rooms/remove/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    global rooms
    rooms = [r for r in rooms if r['id'] != room_id]
    return jsonify({'message': 'Room deleted successfully'}), 200