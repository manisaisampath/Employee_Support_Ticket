from flask import Flask
from app.config import Config
from app.database import close_db


def create_app(config_class=Config):
    """Application factory for the Employee Support Ticket System."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register database connection teardown
    app.teardown_appcontext(close_db)

    # Note: Blueprints and error handlers will be registered in subsequent phases.

    return app
