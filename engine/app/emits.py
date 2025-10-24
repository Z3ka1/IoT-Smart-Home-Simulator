from flask import Blueprint, request, jsonify

emits_bp = Blueprint('emits', __name__)

def _emit_and_respond(event_name, payload):
    from app import socketio
    try:
        socketio.emit(event_name, payload, namespace='/')
        active_clients = len(socketio.server.manager.rooms.get('/', []))
        return jsonify({
            'status': 'success',
            'active_clients': active_clients
        })
    except Exception as e:
        return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

@emits_bp.route('/emit-status', methods=['POST'])
def emit_status():
    data = request.get_json()
    return _emit_and_respond('device_status', {
        'id': data['id'],
        'available': data['available']
    })

@emits_bp.route('/emit-motion_detected', methods=['POST'])
def emit_motion_detected():
    data = request.get_json()
    return _emit_and_respond('motion_detected', {
        'id': data['id'],
        'motion_detected': data['motion_detected']
    })

@emits_bp.route('/emit-weather_station_measurements', methods=['POST'])
def emit_weather_station_measurements():
    data = request.get_json()
    return _emit_and_respond('weather_station_measurements', data)

@emits_bp.route('/emit-simpleled_state', methods=['POST'])
def emit_simpleled_state():
    data = request.get_json()
    return _emit_and_respond('simpleled_state', data)

@emits_bp.route('/emit-lcddisplay_state', methods=['POST'])
def emit_lcddisplay_state():
    data = request.get_json()
    return _emit_and_respond('lcddisplay_state', data)

@emits_bp.route('/emit-lcddisplay_text', methods=['POST'])
def emit_lcddisplay_text():
    data = request.get_json()
    return _emit_and_respond('lcddisplay_text', data)

@emits_bp.route('/emit-lcddisplay_theme', methods=['POST'])
def emit_lcddisplay_theme():
    data = request.get_json()
    return _emit_and_respond('lcddisplay_theme', data)

@emits_bp.route('/emit-rgbstrip_state', methods=['POST'])
def emit_rgbstrip_state():
    data = request.get_json()
    return _emit_and_respond('rgbstrip_state', data)

@emits_bp.route('/emit-rgbstrip_color', methods = ['POST'])
def emit_rgbstrip_color():
    data = request.get_json()
    return _emit_and_respond('rgbstrip_color', data)

@emits_bp.route('/emit-rgbstrip_brightness', methods = ['POST'])
def emit_rgbstrip_brightness():
    data = request.get_json()
    return _emit_and_respond('rgbstrip_brightness', data)

@emits_bp.route('/emit-alarmsensor_enabled', methods = ['POST'])
def emit_alarmsensor_enabled():
    data = request.get_json()
    return _emit_and_respond('alarmsensor_enabled', data)