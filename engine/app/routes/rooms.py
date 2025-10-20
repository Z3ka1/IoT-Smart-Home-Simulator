from flask import Blueprint, jsonify, request
from app.models.room import Room
from app.models.gateway import Gateway
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