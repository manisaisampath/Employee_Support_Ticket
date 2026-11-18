"""Authentication routes for login and logout."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.models import get_user_by_username
from app.security import generate_csrf_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login for both employees and support staff."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = get_user_by_username(username)

        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid username or password.', 'error')
            return render_template('auth/login.html'), 401

        # Clear session to prevent session fixation attacks
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']

        # Generate a fresh CSRF token for the authenticated session
        generate_csrf_token()

        if user['role'] == 'support_staff':
            return redirect('/support/dashboard')
        return redirect('/employee/dashboard')

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Terminate the authenticated session and redirect to login."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
