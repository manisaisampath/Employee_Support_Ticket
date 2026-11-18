"""Security and CSRF protection utilities.

Generates and validates cryptographically secure CSRF tokens per session
using constant-time comparison to protect all state-changing POST requests.
"""

import hmac
import secrets
from flask import abort, request, session


def generate_csrf_token():
    """Generate or retrieve a cryptographically secure CSRF token for the session."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']


def validate_csrf_token():
    """Validate incoming CSRF token against session token using constant-time comparison.

    Rejects missing or invalid tokens on state-changing requests with HTTP 400.
    """
    if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
        token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
        session_token = session.get('_csrf_token')

        if not token or not session_token or not hmac.compare_digest(token, session_token):
            abort(400, description="Invalid or missing CSRF token.")
