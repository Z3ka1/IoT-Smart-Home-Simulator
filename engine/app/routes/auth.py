from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from ..models.gateway import Gateway
from ..utils.jwt_utils import generate_access_token, generate_refresh_token, decode_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    gateway = Gateway.query.filter_by(name=name).first()

    if not gateway:
        return jsonify({"message": "Invalid credentials", "authenticated": False}), 401

    if check_password_hash(gateway.password_hash, password):
        access_token = generate_access_token(gateway.id)
        refresh_token = generate_refresh_token(gateway.id)
        
        return jsonify({
            "message": "Login successful",
            "authenticated": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "gateway_id": gateway.id,
            "gateway_name": gateway.name
        }), 200

    return jsonify({"message": "Invalid credentials", "authenticated": False}), 401

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'error': 'Refresh token is required'}), 400
    
    payload = decode_token(refresh_token)
    if not payload:
        return jsonify({'error': 'Invalid or expired refresh token'}), 401
    
    if payload.get('type') != 'refresh':
        return jsonify({'error': 'Invalid token type'}), 401
    
    # Generate new access token
    gateway_id = payload['gateway_id']
    new_access_token = generate_access_token(gateway_id)
    
    return jsonify({
        'access_token': new_access_token
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({'error': 'Name and password required'}), 400

    existing = Gateway.query.filter_by(name=name).first()
    if existing:
        return jsonify({'error': 'Gateway already exists'}), 409

    new_gateway = Gateway(name=name)
    new_gateway.set_password(password)

    db.session.add(new_gateway)
    db.session.commit()

    return jsonify({'message': 'Gateway registered successfully'}), 201