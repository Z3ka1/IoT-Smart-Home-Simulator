from flask import Blueprint, jsonify, request
from app.models.gateway import Gateway
from app import db

gateways_bp = Blueprint('gateways', __name__)

