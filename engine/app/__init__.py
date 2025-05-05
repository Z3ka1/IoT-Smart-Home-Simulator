from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('app.config.Config')
    
    CORS(app)
    db.init_app(app)

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

    return app
