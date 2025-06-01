from app import create_app, socketio

app = create_app()

@app.route('/emit-status', methods=['POST'])
def emit_status():
    from flask import request, jsonify
    try:
        data = request.get_json()
        socketio.emit('device_status', {
            'id': data['id'],
            'available': data['available']
        }, namespace='/')
        
        # Return the number of active clients
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


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port = 8000)