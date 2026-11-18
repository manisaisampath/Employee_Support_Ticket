from flask import Flask, redirect, session, url_for
from app.config import Config
from app.database import close_db
from app.security import generate_csrf_token, validate_csrf_token


def create_app(config_class=Config):
    """Application factory for the Employee Support Ticket System."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register database connection teardown
    app.teardown_appcontext(close_db)

    # Register CSRF protection on state-changing requests
    app.before_request(validate_csrf_token)

    # Register template context processor for CSRF tokens
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf_token)

    # Root route redirect
    @app.route('/')
    def index():
        if 'user_id' in session:
            if session.get('role') == 'support_staff':
                return redirect('/support/dashboard')
            return redirect('/employee/dashboard')
        return redirect(url_for('auth.login'))

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.employee import employee_bp
    from app.routes.support import support_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(support_bp)

    return app
