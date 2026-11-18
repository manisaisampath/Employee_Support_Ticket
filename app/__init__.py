from flask import Flask, redirect, render_template, session, url_for
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

    # Error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/error.html',
                               code=400,
                               title='Bad Request',
                               description='The server could not process your request.'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/error.html',
                               code=403,
                               title='Access Forbidden',
                               description='You do not have permission to access this resource.'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/error.html',
                               code=404,
                               title='Page Not Found',
                               description='The page or resource you requested could not be found.'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/error.html',
                               code=500,
                               title='Internal Server Error',
                               description='Something went wrong on our end. Please try again later.'), 500

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.employee import employee_bp
    from app.routes.support import support_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(support_bp)

    return app
