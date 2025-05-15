from app import db
from sqlalchemy.dialects.postgresql import JSONB

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    type = db.Column(db.String(50), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    gateway_id = db.Column(db.Integer, db.ForeignKey('gateways.id'), nullable=False)
    properties = db.Column(JSONB)

    room = db.relationship('Room', backref=db.backref('devices', lazy=True))
