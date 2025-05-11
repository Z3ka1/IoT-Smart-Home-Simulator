from flask import Blueprint, jsonify, request
from app.models.room import Room
from app.models.gateway import Gateway
from app import db

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    gateway_id = request.headers.get('X-Gateway-ID')
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401

    gateway = Gateway.query.get(gateway_id)
    if not gateway:
        return jsonify({'error': 'Invalid gateway'}), 401

    rooms = Room.query.filter_by(gateway_id = gateway_id).all()
    return jsonify([{"id": r.id, "gateway_id": r.gateway_id, "name": r.name} for r in rooms])

@rooms_bp.route('/rooms', methods=['POST'])
def add_room():
    data = request.get_json()
    new_room = Room(name=data['name'], gateway_id = data['gatewayId'])
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"id": new_room.id, "name": new_room.name, "gateway_id": new_room.gateway_id}), 201

@rooms_bp.route('/rooms/remove/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted successfully'}), 200