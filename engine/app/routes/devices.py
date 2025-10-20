from flask import Blueprint, jsonify, request
from app.models.device import Device
from app.models.gateway import Gateway
from app import db
from threading import Event
from datetime import datetime, timedelta
import time
import sys
import requests
from ..utils.jwt_utils import token_required

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/devices', methods=['GET'])
@token_required
def get_devices():
    gateway_id = request.gateway_id # Get ID from JWT token

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
            "available": d.available,
            "properties": d.properties
        } for d in devices
    ])


# Temporary in-memory storage for pending pairings
pending_pairing = None  # holds a dict or None

@devices_bp.route('/start-pairing', methods=['POST'])
@token_required
def start_pairing():
    global pending_pairing
    data = request.get_json()

    device_name = data.get('name')
    description = data.get('description', '')  # Optional
    room_id = data.get('room_id')
    gateway_id = request.gateway_id

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

    return jsonify({"message": "Device successfully registered", "device_id": new_device.id}), 201


# Route for any device to ping server in order to keep its frontend widget alive
# Used when device doesnt have property that is changed trough web interface
@devices_bp.route('/devices/<int:device_id>/ping', methods=['GET'])
def device_ping(device_id):
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    device.last_seen = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'ok'}), 200

#region simpleLED
@devices_bp.route('/devices/simpleled/<int:device_id>/state', methods=['PUT'])
@token_required
def update_device_state(device_id):
    gateway_id = request.gateway_id
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    device = Device.query.filter_by(id = device_id, gateway_id=gateway_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()
    if 'state' not in data:
        return jsonify({'error': 'Missing "state" field in request'}), 400
    
    if data['state'] == True:
        state = "on"
    else:
        state = "off"
    properties = device.properties or {}
    properties['state'] = state

    device.properties = properties
    db.session.commit()

    #print(f"props: {properties}", file = sys.stdout)
    #print(f"props: {device.properties}", file = sys.stdout)
    return jsonify({'message': 'Device state updated successfully', 'properties': properties}), 200

@devices_bp.route('/devices/simpleled/<int:device_id>/state', methods=['GET'])
def get_device_state(device_id):
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    device.last_seen = datetime.utcnow()
    db.session.commit()
    return jsonify({'properties': device.properties or {}}), 200

#endregion

#region alarmSensor
@devices_bp.route('/devices/alarmsensor/<int:device_id>/alarm_enabled', methods=['PUT'])
@token_required
def update_is_alarm_enabled(device_id):
    gateway_id = request.gateway_id
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    device = Device.query.filter_by(id = device_id, gateway_id=gateway_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()
    if 'is_alarm_enabled' not in data:
        return jsonify({'error': 'Missing "is_alarm_enabled" field in request'}), 400
    
    properties = device.properties or {}
    properties['is_alarm_enabled'] = data['is_alarm_enabled']

    device.properties = properties
    db.session.commit()

    #print(f"props: {properties}", file = sys.stdout)
    #print(f"props: {device.properties}", file = sys.stdout)
    return jsonify({'message': 'Device state updated successfully', 'properties': properties}), 200

@devices_bp.route('/devices/alarmsensor/<int:device_id>/alarm_enabled', methods = ['GET'])
def get_is_alarm_enabled(device_id):
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    device.last_seen = datetime.utcnow()
    db.session.commit()
    return jsonify({'properties':device.properties or {}}), 200

@devices_bp.route('/devices/alarmsensor/<int:device_id>/motion_detected', methods = ['PUT'])
def update_motion_detected(device_id):
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    device.last_seen = datetime.utcnow()

    data = request.get_json()
    unpackedProps = data['properties']
    properties = device.properties or {}
    properties['motion_detected'] = unpackedProps['motion_detected']

    device.properties = properties
    db.session.commit()

    try:
        response = requests.post(
            f'http://localhost:8000/emit-motion_detected',
            json={
                'id': device.id,
                'motion_detected': properties['motion_detected']
            }
        )
        print(f"Emission status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Failed to trigger emission: {str(e)}")
    
    #print(f"props: {device.properties}", file = sys.stdout)
    return jsonify({'message': 'Device state updated successfully'}), 200

#endregion

#region RGBStrip
@devices_bp.route('/devices/rgbstrip/<int:device_id>/poll_properties', methods = ['GET'])
def get_rgb_strip_properties(device_id):
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    device.last_seen = datetime.utcnow()
    db.session.commit()
    return jsonify({'properties': device.properties or {}}), 200

@devices_bp.route('/devices/rgbstrip/<int:device_id>/state', methods = ['PUT'])
@token_required
def update_rgb_strip_state(device_id):
    gateway_id = request.gateway_id
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    device = Device.query.filter_by(id = device_id, gateway_id=gateway_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()

    if 'state' not in data:
        return jsonify({'error': 'Missing "state" field in request'}), 400    
    
    if data['state'] == True:
        state = "on"
    else:
        state = "off"
    properties = device.properties or {}
    properties['state'] = state

    device.properties = properties
    db.session.commit()

    #print(f"props: {properties}", file = sys.stdout)
    #print(f"props: {device.properties}", file = sys.stdout)
    return jsonify({'message': 'Device state updated successfully'}), 200

@devices_bp.route('/devices/rgbstrip/<int:device_id>/color', methods = ['PUT'])
@token_required
def update_rgb_strip_color(device_id):
    gateway_id = request.gateway_id
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    device = Device.query.filter_by(id = device_id, gateway_id=gateway_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()

    if 'red' not in data or 'green' not in data or 'blue' not in data:
        return jsonify({'error': 'Missing "RGB" fields in request'}), 400    
    
    properties = device.properties or {}
    properties['red'] = data['red']
    properties['green'] = data['green']
    properties['blue'] = data['blue']

    device.properties = properties
    db.session.commit()

    #print(f"props: {properties}", file = sys.stdout)
    #print(f"props: {device.properties}", file = sys.stdout)
    return jsonify({'message': 'Device state updated successfully'}), 200

@devices_bp.route('/devices/rgbstrip/<int:device_id>/brightness', methods = ['PUT'])
@token_required
def update_rgb_strip_brightness(device_id):
    gateway_id = request.gateway_id
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    device = Device.query.filter_by(id = device_id, gateway_id=gateway_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()

    if 'brightness' not in data:
        return jsonify({'error': 'Missing "brightness" field in request'}), 400    
    
    properties = device.properties or {}
    properties['brightness'] = data['brightness'] / 100

    device.properties = properties
    db.session.commit()

    return jsonify({'message': 'Device state updated successfully'}), 200

#endregion

#region LCDDisplay
@devices_bp.route('/devices/lcddisplay/<int:device_id>/poll_properties', methods = ['GET'])
def get_lcd_display_properties(device_id):
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    device.last_seen = datetime.utcnow()
    db.session.commit()
    return jsonify({'properties': device.properties or {}}), 200

@devices_bp.route('/devices/lcddisplay/<int:device_id>/state', methods = ['PUT'])
@token_required
def update_lcd_display_state(device_id):
    gateway_id = request.gateway_id
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    device = Device.query.filter_by(id = device_id, gateway_id=gateway_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()

    if 'state' not in data:
        return jsonify({'error': 'Missing "state" field in request'}), 400    
    
    properties = device.properties or {}
    properties['state'] = data['state']

    device.properties = properties
    db.session.commit()

    return jsonify({'message': 'Device state updated successfully'}), 200

@devices_bp.route('/devices/lcddisplay/<int:device_id>/text', methods = ['PUT'])
@token_required
def update_lcd_display_text(device_id):
    gateway_id = request.gateway_id
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    device = Device.query.filter_by(id = device_id, gateway_id=gateway_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()

    if 'first_line_text' not in data:
        return jsonify({'error': 'Missing "first_line_text" field in request'}), 400
    if 'second_line_text' not in data:
        return jsonify({'error': 'Missing "second_line_text" field in request'}), 400
    
    properties = device.properties or {}
    properties['first_line_text'] = data['first_line_text']
    properties['second_line_text'] = data['second_line_text']

    device.properties = properties
    db.session.commit()

    return jsonify({'message': 'Device state updated successfully'}), 200

@devices_bp.route('/devices/lcddisplay/<int:device_id>/theme', methods = ['PUT'])
@token_required
def update_lcd_display_theme(device_id):
    gateway_id = request.gateway_id
    if not gateway_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    device = Device.query.filter_by(id = device_id, gateway_id=gateway_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()

    if 'display_theme' not in data:
        return jsonify({'error': 'Missing "display_theme" field in request'}), 400    
    
    properties = device.properties or {}
    properties['display_theme'] = data['display_theme']

    device.properties = properties
    db.session.commit()

    return jsonify({'message': 'Device state updated successfully'}), 200

#endregion

#region weatherStation
@devices_bp.route('/devices/weatherstation/<int:device_id>/measurements', methods = ['PUT'])
def update_weather_station_measurements(device_id):
    device = Device.query.filter_by(id = device_id).first()
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    device.last_seen = datetime.utcnow()

    data = request.get_json()
    unpackedProps = data['properties']
    properties = device.properties or {}
    properties['temperature'] = unpackedProps['temperature']
    properties['humidity'] = unpackedProps['humidity']
    properties['city'] = unpackedProps['city']
    properties['api_temperature'] = unpackedProps['api_temperature']
    properties['api_weather_description'] = unpackedProps['api_weather_description']
    properties['api_feels_like'] = unpackedProps['api_feels_like']
    properties['api_pressure'] = unpackedProps['api_pressure']
    properties['api_humidity'] = unpackedProps['api_humidity']
    utc_time = datetime.utcnow() + timedelta(hours=2)
    properties['last_measurement'] = utc_time.strftime('%d.%m %H:%M:%S')

    device.properties = properties
    db.session.commit()

    try:
        response = requests.post(
            f'http://localhost:8000/emit-weather_station_measurements',
            json={
                'id': device.id,
                'temperature': properties['temperature'],
                'humidity': properties['humidity'],
                'city': properties['city'],
                'api_temperature': properties['api_temperature'],
                'api_weather_description': properties['api_weather_description'],
                'api_feels_like': properties['api_feels_like'],
                'api_pressure': properties['api_pressure'],
                'api_humidity': properties['api_humidity'],
                'last_measurement': properties['last_measurement']
            }
        )
        print(f"Emission status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Failed to trigger emission: {str(e)}")
    
    #print(f"props: {device.properties}", file = sys.stdout)
    return jsonify({'message': 'Device measurements updated'}), 200


#endregion