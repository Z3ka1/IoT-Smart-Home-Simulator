from flask import Blueprint, jsonify, request
from app.models.device import Device
from app.models.gateway import Gateway
from app import db
from threading import Event
import time

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/devices', methods=['GET'])
def get_devices():
    gateway_id = request.headers.get('X-Gateway-ID')
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401

    gateway = Gateway.query.get(gateway_id)
    if not gateway:
        return jsonify({'error': 'Invalid gateway'}), 401

    devices = Device.query.filter_by(gateway_id = gateway_id).all()
    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "type": d.type,
            "description": d.description,
            "roomId": d.room_id,
            "properties": d.properties
        } for d in devices
    ])


# Temporary in-memory storage for pending pairings
pending_pairing = None  # holds a dict or None

@devices_bp.route('/start-pairing', methods=['POST'])
def start_pairing():
    global pending_pairing
    data = request.get_json()

    device_name = data.get('name')
    description = data.get('description', '')  # Optional
    room_id = data.get('room_id')
    gateway_id = request.headers.get('X-Gateway-ID')

    if not all([gateway_id, device_name, room_id]):
        return jsonify({"message": "Missing data"}), 400

    if pending_pairing is not None:
        return jsonify({"message": "Another pairing is already in progress"}), 409

    pairing_event = Event()
    pending_pairing = {
        "name": device_name,
        "description": description,
        "room_id": room_id,
        "gateway_id": gateway_id,
        "event": pairing_event,
        "type": None,
        "properties": None
    }

    # If time changes, also change PairDeviceView.vue/pairingDuration
    paired = pairing_event.wait(timeout=60)

    if paired:
        return jsonify({"message": "Device paired successfully"}), 200
    else:
        pending_pairing = None
        return jsonify({"message": "Pairing timed out"}), 408


@devices_bp.route('/pair-device', methods=['POST'])
def pair_device():
    global pending_pairing
    if pending_pairing is None:
        return jsonify({"message": "No pending pairing found"}), 404

    data = request.get_json()
    device_type = data.get('type')
    properties = data.get('properties', {})

    # Complete pairing info
    pending_pairing["type"] = device_type
    pending_pairing["properties"] = properties

    new_device = Device(
        name=pending_pairing["name"],
        type=device_type,
        description=pending_pairing["description"],
        room_id=pending_pairing["room_id"],
        gateway_id=pending_pairing["gateway_id"],
        properties=properties
    )
    db.session.add(new_device)
    db.session.commit()

    pending_pairing["event"].set()
    pending_pairing = None

    return jsonify({"message": "Device successfully registered"}), 201