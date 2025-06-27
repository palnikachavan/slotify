from flask import Flask
from app.config import Config
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models for migration discovery
    from app.models import tenant, slot, service, slot_user

    # Register routes
    from app.routes.auth_routes import auth_bp
    from app.routes.booking_routes import booking_bp
    from app.routes.user_auth_routes import user_auth_bp
    from app.routes.user_booking_routes import user_booking_bp
    from app.routes.admin_routes import admin_bp
    
    app.register_blueprint(admin_bp, url_prefix='/admin')

    app.register_blueprint(user_auth_bp, url_prefix='/user/auth')
    app.register_blueprint(user_booking_bp, url_prefix='/user/bookings')

    app.register_blueprint(auth_bp, url_prefix="/tenant/auth")
    app.register_blueprint(booking_bp, url_prefix="/tenant/bookings")

    return app
