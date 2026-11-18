"""Database seeding script for Employee Support Ticket System.

Populates initial accounts and sample tickets in an idempotent, repeat-safe manner.
Passwords are never hardcoded or printed, and are hashed using Werkzeug.
"""

import getpass
import os
import sys
from werkzeug.security import generate_password_hash

from app import create_app
from app.database import init_db
from app.models import (
    create_ticket,
    create_user,
    get_current_utc_timestamp,
    get_ticket_by_title_and_user,
    get_user_by_username,
)

SAMPLE_TICKETS = [
    {
        "title": "Laptop not charging",
        "category": "Hardware",
        "priority": "High",
        "status": "Open",
        "description": "The laptop battery does not hold charge and the device shuts down immediately when unplugged from the AC adapter.",
    },
    {
        "title": "Cannot log in to VPN",
        "category": "Network",
        "priority": "High",
        "status": "In Progress",
        "description": "Receiving authentication timeout error when attempting to connect to the corporate VPN from home network.",
    },
    {
        "title": "Need access to shared project folder",
        "category": "Access",
        "priority": "Medium",
        "status": "Open",
        "description": "Requesting read and write permissions to the shared team project folder for Q4 planning documentation.",
    },
    {
        "title": "Excel keeps crashing on startup",
        "category": "Software",
        "priority": "Medium",
        "status": "Resolved",
        "description": "Microsoft Excel terminates unexpectedly with an unhandled exception immediately after launching.",
    },
    {
        "title": "Request a second monitor",
        "category": "Hardware",
        "priority": "Low",
        "status": "Closed",
        "description": "Requesting an additional external monitor and HDMI cable for dual-display workstation setup.",
    },
]


def resolve_password(username, role, env_keys):
    """Retrieve password from environment variables or interactive prompt.

    Never prints or hardcodes the password.
    """
    for key in env_keys:
        pwd = os.environ.get(key)
        if pwd:
            return pwd

    if sys.stdin.isatty():
        prompt_text = f"Enter password for {role} account '{username}': "
        pwd = getpass.getpass(prompt_text)
        if pwd:
            return pwd

    keys_str = ", ".join(env_keys)
    raise ValueError(
        f"Password for user '{username}' ({role}) could not be determined. "
        f"Please set one of these environment variables: [{keys_str}] or run interactively."
    )


def seed_database(app=None):
    """Seed the database with verified initial accounts and sample tickets."""
    if app is None:
        app = create_app()

    with app.app_context():
        # Ensure schema tables exist before seeding
        init_db()

        print("--- Starting Database Seeding ---")

        # 1. Seed Accounts
        accounts = [
            {
                "username": "ravi",
                "role": "employee",
                "env_keys": ["SEED_RAVI_PASSWORD", "DEFAULT_EMP_PASSWORD", "SEED_PASSWORD"],
            },
            {
                "username": "support_admin",
                "role": "support_staff",
                "env_keys": ["SEED_SUPPORT_PASSWORD", "DEFAULT_STAFF_PASSWORD", "SEED_PASSWORD"],
            },
        ]

        user_ids = {}

        for acc in accounts:
            existing = get_user_by_username(acc["username"])
            if existing:
                print(f"User '{acc['username']}' already exists (ID: {existing['id']}). Skipping insertion to preserve credentials.")
                user_ids[acc["username"]] = existing["id"]
            else:
                raw_pwd = resolve_password(acc["username"], acc["role"], acc["env_keys"])
                hashed_pwd = generate_password_hash(raw_pwd)
                user_id = create_user(
                    username=acc["username"],
                    password_hash=hashed_pwd,
                    role=acc["role"],
                    created_date=get_current_utc_timestamp(),
                )
                print(f"User '{acc['username']}' ({acc['role']}) created successfully (ID: {user_id}).")
                user_ids[acc["username"]] = user_id

        # 2. Seed Sample Tickets (Linked to ravi)
        ravi_id = user_ids.get("ravi")
        if not ravi_id:
            raise RuntimeError("Cannot seed tickets because user 'ravi' was not found or created.")

        tickets_created_count = 0
        tickets_skipped_count = 0

        for ticket_data in SAMPLE_TICKETS:
            existing_ticket = get_ticket_by_title_and_user(ticket_data["title"], ravi_id)
            if existing_ticket:
                tickets_skipped_count += 1
            else:
                timestamp = get_current_utc_timestamp()
                create_ticket(
                    title=ticket_data["title"],
                    description=ticket_data["description"],
                    category=ticket_data["category"],
                    priority=ticket_data["priority"],
                    status=ticket_data["status"],
                    created_by=ravi_id,
                    created_date=timestamp,
                    last_updated_date=timestamp,
                )
                tickets_created_count += 1

        print(f"Sample Tickets: {tickets_created_count} inserted, {tickets_skipped_count} skipped (already existed).")
        print("--- Seeding Completed Successfully ---")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as exc:
        print(f"Seeding failed: {exc}", file=sys.stderr)
        sys.exit(1)
