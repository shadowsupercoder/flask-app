from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    """Construct the core application."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_url_path="",
        static_folder="static")
    app.config.from_object('config.DevelopmentConfig')
    Bootstrap(app)
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        from app.payment.controllers import module  # Import routes
        db.create_all()  # Create sql tables for our data models
        app.url_map.strict_slashes = False
        app.register_blueprint(module)
        return app
