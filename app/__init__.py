from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(
        __name__,
        template_folder="templates")
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)

    with app.app_context():
        from app.payment.controllers import module  # Import routes
        db.create_all()  # Create sql tables for our data models
        app.url_map.strict_slashes = False
        app.register_blueprint(module)
        return app
