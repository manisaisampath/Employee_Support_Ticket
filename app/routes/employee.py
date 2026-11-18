"""Employee routes for ticket dashboard, ticket creation, details, and commenting."""

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from app.decorators import login_required, role_required
from app.models import (
    add_comment,
    create_ticket,
    get_comments_by_ticket,
    get_ticket_by_id,
    get_tickets_by_user,
)

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

ALLOWED_CATEGORIES = ('Hardware', 'Software', 'Network', 'Access', 'Other')
ALLOWED_PRIORITIES = ('Low', 'Medium', 'High')


@employee_bp.route('/dashboard')
@login_required
@role_required('employee')
def dashboard():
    """Display the employee's personal ticket dashboard."""
    user_id = session['user_id']
    tickets = get_tickets_by_user(user_id)
    return render_template('employee/dashboard.html', tickets=tickets)


@employee_bp.route('/tickets/create', methods=['GET', 'POST'])
@login_required
@role_required('employee')
def create():
    """Handle new support ticket creation with server-side validation."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        priority = request.form.get('priority', '').strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        elif len(title) > 100:
            errors.append("Title cannot exceed 100 characters.")

        if not description:
            errors.append("Description cannot be empty.")

        if category not in ALLOWED_CATEGORIES:
            errors.append("Invalid category selected.")

        if priority not in ALLOWED_PRIORITIES:
            errors.append("Invalid priority selected.")

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template(
                'employee/create.html',
                title_val=title,
                description_val=description,
                category_val=category,
                priority_val=priority,
                categories=ALLOWED_CATEGORIES,
                priorities=ALLOWED_PRIORITIES,
            ), 400

        # Always bind created_by to logged-in user, initial status Open (PA-04)
        create_ticket(
            title=title,
            description=description,
            category=category,
            priority=priority,
            status='Open',
            created_by=session['user_id'],
        )

        flash("Ticket created successfully.", "success")
        return redirect(url_for('employee.dashboard'))

    return render_template(
        'employee/create.html',
        categories=ALLOWED_CATEGORIES,
        priorities=ALLOWED_PRIORITIES,
    )


@employee_bp.route('/tickets/<int:ticket_id>')
@login_required
@role_required('employee')
def detail(ticket_id):
    """Display personal ticket details and comment thread for the employee."""
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        abort(404, description="Ticket not found.")

    # Strictly enforce visibility isolation: employees view only their own tickets
    if ticket['created_by'] != session['user_id']:
        abort(403, description="Access forbidden: You are not authorized to view this ticket.")

    comments = get_comments_by_ticket(ticket_id)
    return render_template('employee/detail.html', ticket=ticket, comments=comments)


@employee_bp.route('/tickets/<int:ticket_id>/comments', methods=['POST'])
@login_required
@role_required('employee')
def comment(ticket_id):
    """Add a permanent comment to the employee's own ticket."""
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        abort(404, description="Ticket not found.")

    # Strictly enforce: employees may comment only on their own tickets
    if ticket['created_by'] != session['user_id']:
        abort(403, description="Access forbidden: You are not authorized to comment on this ticket.")

    content = request.form.get('content', '').strip()
    if not content:
        flash("Comment cannot be empty.", "error")
        comments = get_comments_by_ticket(ticket_id)
        return render_template('employee/detail.html', ticket=ticket, comments=comments), 400

    # Add comment and atomically refresh last_updated_date; allowed on Closed tickets
    add_comment(ticket_id, session['user_id'], content)
    flash("Comment added successfully.", "success")
    return redirect(url_for('employee.detail', ticket_id=ticket_id))
