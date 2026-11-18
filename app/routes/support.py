"""Support staff routes for global ticket management and ticket inspection."""

from flask import Blueprint, abort, render_template
from app.decorators import login_required, role_required
from app.models import get_all_tickets, get_ticket_by_id

support_bp = Blueprint('support', __name__, url_prefix='/support')


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
    """Display complete read-only ticket details for support staff."""
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        abort(404, description="Ticket not found.")
    return render_template('support/detail.html', ticket=ticket)
