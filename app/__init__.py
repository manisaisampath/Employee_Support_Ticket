from flask import Flask
from app.config import Config


def create_app(config_class=Config):
    """Application factory for the Employee Support Ticket System."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Note: Blueprints, database handlers, and error handlers will be registered in subsequent phases.

    return app
