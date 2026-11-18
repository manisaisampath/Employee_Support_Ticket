"""Data access models and helper functions for Employee Support Ticket System.

All database interactions use parameterized queries to prevent SQL injection.
"""

from datetime import datetime, timezone
from app.database import get_db


def get_current_utc_timestamp():
    """Return the current UTC timestamp formatted as YYYY-MM-DD HH:MM:SS."""
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def get_user_by_username(username):
    """Retrieve a user record by username."""
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE username = ?;",
        (username,)
    ).fetchone()


def get_user_by_id(user_id):
    """Retrieve a user record by user ID."""
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?;",
        (user_id,)
    ).fetchone()


def create_user(username, password_hash, role, created_date=None):
    """Create a new user record.

    Returns the integer ID of the created user.
    """
    if created_date is None:
        created_date = get_current_utc_timestamp()
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO users (username, password_hash, role, created_date)
        VALUES (?, ?, ?, ?);
        """,
        (username, password_hash, role, created_date)
    )
    db.commit()
    return cursor.lastrowid


def get_all_users():
    """Retrieve all user records."""
    db = get_db()
    return db.execute("SELECT * FROM users ORDER BY id ASC;").fetchall()


def get_all_tickets():
    """Retrieve all tickets joined with author username, ordered by last_updated_date DESC."""
    db = get_db()
    return db.execute(
        """
        SELECT t.*, u.username AS creator_username
        FROM tickets t
        JOIN users u ON t.created_by = u.id
        ORDER BY t.last_updated_date DESC;
        """
    ).fetchall()


def get_tickets_by_user(user_id):
    """Retrieve tickets created by a specific user, ordered by last_updated_date DESC."""
    db = get_db()
    return db.execute(
        """
        SELECT * FROM tickets
        WHERE created_by = ?
        ORDER BY last_updated_date DESC;
        """,
        (user_id,)
    ).fetchall()


def get_ticket_by_id(ticket_id):
    """Retrieve a single ticket by ID with author details."""
    db = get_db()
    return db.execute(
        """
        SELECT t.*, u.username AS creator_username
        FROM tickets t
        JOIN users u ON t.created_by = u.id
        WHERE t.id = ?;
        """,
        (ticket_id,)
    ).fetchone()


def get_ticket_by_title_and_user(title, user_id):
    """Retrieve a ticket by exact title and author user ID (useful for idempotent operations)."""
    db = get_db()
    return db.execute(
        "SELECT * FROM tickets WHERE title = ? AND created_by = ?;",
        (title, user_id)
    ).fetchone()


def create_ticket(title, description, category, priority, status, created_by, created_date=None, last_updated_date=None):
    """Create a new ticket record.

    Returns the integer ID of the created ticket.
    """
    current_time = get_current_utc_timestamp()
    if created_date is None:
        created_date = current_time
    if last_updated_date is None:
        last_updated_date = created_date

    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO tickets (title, description, category, priority, status, created_by, created_date, last_updated_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (title, description, category, priority, status, created_by, created_date, last_updated_date)
    )
    db.commit()
    return cursor.lastrowid


def update_ticket_status(ticket_id, new_status, last_updated_date=None):
    """Update a ticket's status and refresh last_updated_date."""
    if last_updated_date is None:
        last_updated_date = get_current_utc_timestamp()
    db = get_db()
    db.execute(
        """
        UPDATE tickets
        SET status = ?, last_updated_date = ?
        WHERE id = ?;
        """,
        (new_status, last_updated_date, ticket_id)
    )
    db.commit()


def get_comments_by_ticket(ticket_id):
    """Retrieve all comments for a ticket in chronological order with author details."""
    db = get_db()
    return db.execute(
        """
        SELECT c.*, u.username AS author_username, u.role AS author_role
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.ticket_id = ?
        ORDER BY c.created_date ASC, c.id ASC;
        """,
        (ticket_id,)
    ).fetchall()


def add_comment(ticket_id, user_id, content, created_date=None):
    """Add a permanent comment to a ticket and atomically refresh last_updated_date."""
    if created_date is None:
        created_date = get_current_utc_timestamp()
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO comments (ticket_id, user_id, content, created_date)
        VALUES (?, ?, ?, ?);
        """,
        (ticket_id, user_id, content, created_date)
    )
    db.execute(
        """
        UPDATE tickets
        SET last_updated_date = ?
        WHERE id = ?;
        """,
        (created_date, ticket_id)
    )
    db.commit()
    return cursor.lastrowid


