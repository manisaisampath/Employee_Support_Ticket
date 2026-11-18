-- SQLite Database Schema for Employee Support Ticket Management System

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('employee', 'support_staff')),
    created_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(length(title) > 0 AND length(title) <= 100),
    description TEXT NOT NULL CHECK(length(description) > 0),
    category TEXT NOT NULL CHECK(category IN ('Hardware', 'Software', 'Network', 'Access', 'Other')),
    priority TEXT NOT NULL CHECK(priority IN ('Low', 'Medium', 'High')),
    status TEXT NOT NULL CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    created_by INTEGER NOT NULL,
    created_date TEXT NOT NULL,
    last_updated_date TEXT NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL CHECK(length(trim(content)) > 0),
    created_date TEXT NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES tickets (id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Recommended Indexes
CREATE INDEX IF NOT EXISTS idx_tickets_created_by ON tickets(created_by);
CREATE INDEX IF NOT EXISTS idx_tickets_last_updated ON tickets(last_updated_date DESC);
CREATE INDEX IF NOT EXISTS idx_comments_ticket_id ON comments(ticket_id);
