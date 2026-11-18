"""Support staff routes for global ticket management, inspection, and status updates."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from app.decorators import login_required, role_required
from app.models import get_all_tickets, get_ticket_by_id, update_ticket_status, add_comment, get_comments_by_ticket

support_bp = Blueprint('support', __name__, url_prefix='/support')

ALLOWED_STATUSES = ('Open', 'In Progress', 'Resolved', 'Closed')


@support_bp.route('/dashboard')
@login_required
@role_required('support_staff')
def dashboard():
    """Display the global organization ticket queue for support staff."""
    tickets = get_all_tickets()
    return render_template('support/dashboard.html', tickets=tickets)


@support_bp.route('/tickets/<int:ticket_id>')
@login_required
@role_required('support_staff')
def detail(ticket_id):
    """Display complete read-only ticket details and status update form for support staff."""
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        abort(404, description="Ticket not found.")
    comments = get_comments_by_ticket(ticket_id)
    return render_template(
        'support/detail.html',
        ticket=ticket,
        statuses=ALLOWED_STATUSES,
        comments=comments,
    )


@support_bp.route('/tickets/<int:ticket_id>/status', methods=['POST'])
@login_required
@role_required('support_staff')
def update_status(ticket_id):
    """Update a ticket's status.

    Permits direct flexible transitions between any valid status.
    Automatically refreshes last_updated_date in UTC.
    """
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        abort(404, description="Ticket not found.")

    new_status = request.form.get('status', '').strip()
    if new_status not in ALLOWED_STATUSES:
        abort(400, description="Invalid status selected.")

    update_ticket_status(ticket_id, new_status)

    flash(f"Status for Ticket #{ticket_id} updated to '{new_status}'.", "success")
    return redirect(url_for('support.detail', ticket_id=ticket_id))

# Comment submission for support staff
@support_bp.route('/tickets/<int:ticket_id>/comments', methods=['POST'])
@login_required
@role_required('support_staff')
def add_comment_route(ticket_id):
    """Add a comment to any ticket (support staff)."""
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        abort(404, description="Ticket not found.")
    content = request.form.get('content', '').strip()
    if not content:
        flash('Comment cannot be empty.', 'error')
        # reuse detail view with comments
        comments = get_comments_by_ticket(ticket_id)
        return render_template('support/detail.html', ticket=ticket, statuses=ALLOWED_STATUSES, comments=comments), 400
    add_comment(ticket_id, session['user_id'], content)
    flash('Comment added successfully.', 'success')
    return redirect(url_for('support.detail', ticket_id=ticket_id))
