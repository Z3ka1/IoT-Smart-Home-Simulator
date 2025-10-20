from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
import sys
import requests
import os

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins = "*")#, logger = True, engineio_logger = True)

class Config:
    from app.config import Config as BaseConfig
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = BaseConfig.SQLALCHEMY_TRACK_MODIFICATIONS
    port = BaseConfig.port
    JWT_SECRET_KEY = BaseConfig.JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = BaseConfig.JWT_ACCESS_TOKEN_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = BaseConfig.JWT_REFRESH_TOKEN_EXPIRES

scheduler = APScheduler()

def update_device_availability():
    from app.models.device import Device
    
    
    with scheduler.app.app_context():
        now = datetime.utcnow()
        timeout = timedelta(seconds=30)
        
        port = scheduler.app.config.get('port', 8000)
        
        devices = Device.query.all()
        for device in devices:
            # print(f"\n=== Checking device {device.id} ===")
            # print(f"Last seen: {device.last_seen}")
            # print(f"Current time: {now}")
            # print(f"Time difference: {now - device.last_seen if device.last_seen else 'Never'}")
            is_actually_online = device.last_seen and (now - device.last_seen <= timeout)

            if not is_actually_online and device.available:
                if device.available:
                    print(f"Marking device {device.id} as OFFLINE")
                    device.available = False
                    db.session.commit()
                    # HTTP POST to trigger emission
                    try:
                        response = requests.post(
                            f'http://localhost:{port}/emit-status',
                            json={
                                'id': device.id,
                                'available': False
                            }
                        )
                        print(f"Emission status: {response.status_code}, Response: {response.json()}")
                    except Exception as e:
                        print(f"Failed to trigger emission: {str(e)}")
            elif is_actually_online and not device.available:
                print(f"Marking device {device.id} as ONLINE")
                device.available = True
                db.session.commit()
                try:
                    response = requests.post(
                        f'http://localhost:{port}/emit-status',
                        json={
                            'id': device.id,
                            'available': True
                        }
                    )
                    print(f"Emission status: {response.status_code}, Response: {response.json()}")
                except Exception as e:
                    print(f"Failed to trigger emission: {str(e)}")


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    from app.routes.rooms import rooms_bp
    from app.routes.devices import devices_bp
    from app.routes.gateways import gateways_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(rooms_bp, url_prefix='/api')
    app.register_blueprint(devices_bp, url_prefix='/api')
    app.register_blueprint(gateways_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    # Scheduler starts in 2 processes when debug = true, this if ensures just one process of scheduler
    # Make sure scheduler creates when debug = false
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print(f"\n Initializing scheduler in PID: {os.getpid()}, Main: {os.environ.get('WERKZEUG_RUN_MAIN')}\n")
        scheduler.init_app(app)
        scheduler.start()
        scheduler.add_job(id='check_device_availability', func=update_device_availability, trigger='interval', seconds=15)
        
    return app