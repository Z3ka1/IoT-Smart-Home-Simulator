from app import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    type = db.Column(db.String(50), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    gateway_id = db.Column(db.Integer, db.ForeignKey('gateways.id'), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    available = db.Column(db.Boolean, default=False)
    properties = db.Column(MutableDict.as_mutable(JSONB))

    room = db.relationship('Room', backref=db.backref('devices', lazy=True))
