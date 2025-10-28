from app import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime

class Scene(db.Model):
    __tablename__ = 'scenes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    gateway_id = db.Column(db.Integer, db.ForeignKey('gateways.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)  # Optional: scene for specific room
    device_configurations = db.Column(MutableDict.as_mutable(JSONB))  # {device_id: {properties}}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    gateway = db.relationship('Gateway', backref=db.backref('scenes', lazy=True))
    room = db.relationship('Room', backref=db.backref('scenes', lazy=True))
