from flask import Blueprint, jsonify, request
from app.models.scene import Scene
from app.models.device import Device
from app.models.gateway import Gateway
from app import db
from ..utils.jwt_utils import token_required
import requests

scenes_bp = Blueprint('scenes', __name__)

@scenes_bp.route('/scenes', methods=['GET'])
@token_required
def get_scenes():
    gateway_id = request.gateway_id
    
    gateway = Gateway.query.get(gateway_id)
    if not gateway:
        return jsonify({'error': 'Invalid gateway'}), 401
    
    scenes = Scene.query.filter_by(gateway_id=gateway_id).all()
    return jsonify([
        {
            'id': s.id,
            'name': s.name,
            'description': s.description,
            'roomId': s.room_id,
            'deviceConfigurations': s.device_configurations,
            'createdAt': s.created_at.isoformat() if s.created_at else None,
            'updatedAt': s.updated_at.isoformat() if s.updated_at else None
        } for s in scenes
    ]), 200

@scenes_bp.route('/scenes', methods=['POST'])
@token_required
def create_scene():
    gateway_id = request.gateway_id
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description', '')
    room_id = data.get('roomId')
    device_configurations = data.get('deviceConfigurations', {})
    
    if not name:
        return jsonify({'error': 'Scene name is required'}), 400
    
    # Validate that all devices belong to this gateway
    device_ids = [int(device_id) for device_id in device_configurations.keys()]
    devices = Device.query.filter(Device.id.in_(device_ids), Device.gateway_id == gateway_id).all()
    
    if len(devices) != len(device_ids):
        return jsonify({'error': 'Some devices do not belong to this gateway'}), 403
    
    new_scene = Scene(
        name=name,
        description=description,
        gateway_id=gateway_id,
        room_id=room_id,
        device_configurations=device_configurations
    )
    
    db.session.add(new_scene)
    db.session.commit()
    
    return jsonify({
        'id': new_scene.id,
        'name': new_scene.name,
        'description': new_scene.description,
        'roomId': new_scene.room_id,
        'deviceConfigurations': new_scene.device_configurations,
        'message': 'Scene created successfully'
    }), 201

@scenes_bp.route('/scenes/<int:scene_id>', methods=['PUT'])
@token_required
def update_scene(scene_id):
    gateway_id = request.gateway_id
    data = request.get_json()
    
    scene = Scene.query.filter_by(id=scene_id, gateway_id=gateway_id).first()
    if not scene:
        return jsonify({'error': 'Scene not found'}), 404
    
    if 'name' in data:
        scene.name = data['name']
    if 'description' in data:
        scene.description = data['description']
    if 'roomId' in data:
        scene.room_id = data['roomId']
    if 'deviceConfigurations' in data:
        # Validate that all devices belong to this gateway
        device_ids = [int(device_id) for device_id in data['deviceConfigurations'].keys()]
        devices = Device.query.filter(Device.id.in_(device_ids), Device.gateway_id == gateway_id).all()
        
        if len(devices) != len(device_ids):
            return jsonify({'error': 'Some devices do not belong to this gateway'}), 403
        
        scene.device_configurations = data['deviceConfigurations']
    
    db.session.commit()
    
    return jsonify({
        'id': scene.id,
        'name': scene.name,
        'description': scene.description,
        'roomId': scene.room_id,
        'deviceConfigurations': scene.device_configurations,
        'message': 'Scene updated successfully'
    }), 200

@scenes_bp.route('/scenes/<int:scene_id>', methods=['DELETE'])
@token_required
def delete_scene(scene_id):
    gateway_id = request.gateway_id
    
    scene = Scene.query.filter_by(id=scene_id, gateway_id=gateway_id).first()
    if not scene:
        return jsonify({'error': 'Scene not found'}), 404
    
    db.session.delete(scene)
    db.session.commit()
    
    return jsonify({'message': 'Scene deleted successfully'}), 200

@scenes_bp.route('/scenes/<int:scene_id>/activate', methods=['POST'])
@token_required
def activate_scene(scene_id):
    gateway_id = request.gateway_id
    
    scene = Scene.query.filter_by(id=scene_id, gateway_id=gateway_id).first()
    if not scene:
        return jsonify({'error': 'Scene not found'}), 404
    
    if not scene.device_configurations:
        return jsonify({'error': 'Scene has no device configurations'}), 400
    
    updated_devices = []
    errors = []
    
    for device_id_str, properties in scene.device_configurations.items():
        device_id = int(device_id_str)
        device = Device.query.filter_by(id=device_id, gateway_id=gateway_id).first()
        
        if not device:
            errors.append(f'Device {device_id} not found')
            continue
            
        # If device is not currently online, skip
        if device.available == False:
            continue
        
        # Update properties
        current_properties = device.properties or {}
        current_properties.update(properties)
        device.properties = current_properties
        
        updated_devices.append({
            'id': device.id,
            'name': device.name,
            'type': device.type,
            'properties': device.properties
        })
    
    db.session.commit()
    emit_device_updates_for_scene(updated_devices)
    
    return jsonify({
        'message': 'Scene activated successfully',
        'updatedDevices': updated_devices,
        'errors': errors if errors else None
    }), 200


def emit_device_updates_for_scene(updated_devices):
    base_url = f"http://localhost:8000"
    
    for device_data in updated_devices:
        device_id = device_data['id']
        properties = device_data['properties']
        device_type = device_data['type']
        
        try:
            # Simple LED
            if device_type.lower() == 'simpleled':
                if 'state' in properties:
                    requests.post(
                        f"{base_url}/emit-simpleled_state",
                        json={
                            'id': device_id,
                            'state': properties['state']
                        },
                        timeout=2
                    )
            # RGB Strip
            elif device_type.lower() == 'rgbstrip':
                if 'state' in properties:
                    requests.post(
                        f"{base_url}/emit-rgbstrip_state",
                        json={
                            'id': device_id,
                            'state': properties['state']
                        },
                        timeout=2
                    )
                if 'red' in properties or 'green' in properties or 'blue' in properties:
                    requests.post(
                        f"{base_url}/emit-rgbstrip_color",
                        json={
                            'id': device_id,
                            'red': properties.get('red', 0),
                            'green': properties.get('green', 0),
                            'blue': properties.get('blue', 0)
                        },
                        timeout=2
                    )
                if 'brightness' in properties:
                    requests.post(
                        f"{base_url}/emit-rgbstrip_brightness",
                        json={
                            'id': device_id,
                            'brightness': properties.get('brightness', 100)
                        },
                        timeout=2
                    )
            # LCD Display
            elif device_type.lower() == 'lcddisplay':
                if 'state' in properties:
                    requests.post(
                        f"{base_url}/emit-lcddisplay_state",
                        json={
                            'id': device_id,
                            'state': properties['state']
                        },
                        timeout=2
                    )
                if 'first_line_text' in properties or 'second_line_text' in properties:
                    requests.post(
                        f"{base_url}/emit-lcddisplay_text",
                        json={
                            'id': device_id,
                            'first_line_text': properties.get('first_line_text', ''),
                            'second_line_text': properties.get('second_line_text', '')
                        },
                        timeout=2
                    )
                if 'display_theme' in properties:
                    requests.post(
                        f"{base_url}/emit-lcddisplay_theme",
                        json={
                            'id': device_id,
                            'display_theme': properties['display_theme']
                        },
                        timeout=2
                    )
            # Alarm sensor
            elif device_type.lower() == 'alarmsensor':
                if 'is_alarm_enabled' in properties:
                    requests.post(
                        f"{base_url}/emit-alarmsensor_enabled",
                        json={
                            'id': device_id,
                            'is_alarm_enabled': properties['is_alarm_enabled']
                        },
                        timeout=2
                    )
            
            elif device_type.lower() == 'weatherstation':
                pass
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to emit update for device {device_id}: {e}")
            continue