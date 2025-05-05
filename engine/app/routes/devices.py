from flask import Blueprint, jsonify, request
from app.models.device import Device
from app import db

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "type": d.type,
            "roomId": d.room_id,
            "properties": d.properties
        } for d in devices
    ])
