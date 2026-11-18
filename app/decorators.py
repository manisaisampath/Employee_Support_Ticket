"""Authentication and Role-Based Access Control (RBAC) route decorators."""

from functools import wraps
from flask import abort, redirect, session, url_for


def login_required(f):
    """Ensure user is logged in before accessing the route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(allowed_roles):
    """Ensure user possesses one of the allowed roles.

    Returns HTTP 403 Forbidden for authenticated users with insufficient permissions.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            user_role = session.get('role')
            if user_role not in allowed_roles:
                abort(403, description="Access forbidden: Insufficient role permissions.")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
