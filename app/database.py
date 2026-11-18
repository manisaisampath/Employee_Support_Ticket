import os
import sqlite3
from flask import current_app, g


def get_db():
    """Get a database connection for the current application context.

    Enforces SQLite foreign keys and sets sqlite3.Row as the row factory.
    """
    if 'db' not in g:
        db_path = current_app.config['DATABASE']
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db


def close_db(e=None):
    """Safely close the database connection if open."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app=None):
    """Initialize the database schema using schema.sql."""
    if app is not None:
        with app.app_context():
            _execute_schema()
    else:
        _execute_schema()


def _execute_schema():
    """Read and execute schema.sql against the database."""
    db = get_db()
    schema_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        'schema.sql'
    )
    with open(schema_path, 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    db.commit()
