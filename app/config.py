import os
import secrets
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        SECRET_KEY = secrets.token_hex(32)
        print(
            "WARNING: SECRET_KEY environment variable not set. "
            "Generated a secure random key for local development.",
            file=sys.stderr
        )

    DATABASE = os.path.join(basedir, 'support_ticket.db')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
