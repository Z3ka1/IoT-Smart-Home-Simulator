import jwt
from datetime import datetime, timedelta
from flask import current_app
from functools import wraps
from flask import request, jsonify

def generate_access_token(gateway_id):
    # Generate JWT access token for a gateway
    payload = {
        'gateway_id': gateway_id,
        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def generate_refresh_token(gateway_id):
    # Generate JWT refresh token for a gateway
    payload = {
        'gateway_id': gateway_id,
        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_REFRESH_TOKEN_EXPIRES']),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    # Decode and verify JWT token
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    # Decorator to protect routes with JWT authentication
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Decode and verify token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        if payload.get('type') != 'access':
            return jsonify({'error': 'Invalid token type'}), 401
        
        # Add gateway_id to request context
        request.gateway_id = payload['gateway_id']
        
        return f(*args, **kwargs)
    
    return decorated
