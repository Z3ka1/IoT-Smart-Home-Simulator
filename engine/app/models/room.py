from app import db

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    gateway_id = db.Column(db.Integer, db.ForeignKey('gateways.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    devices = db.relationship('Device', back_populates = 'room', cascade = 'all, delete-orphan', passive_deletes = True)