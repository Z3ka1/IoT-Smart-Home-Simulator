from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from ..models.gateway import Gateway

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    gateway = Gateway.query.filter_by(name=name).first()

    if check_password_hash(gateway.password_hash, password):  # Use hashing in production
        return jsonify({"message": "Login successful", "authenticated": True}), 200

    return jsonify({"message": "Invalid credentials", "authenticated": False}), 401

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