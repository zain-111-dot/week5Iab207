# Edited by Zain
from flask import Blueprint, render_template, request
from sqlalchemy import or_

from . import db
from .models import Event


# Main website routes
main_bp = Blueprint('views', __name__)


# TASK #11 - LANDING PAGE AND EVENT LISTING
@main_bp.route('/')
def index():
    # Get optional search and category values
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    # Start with all events
    statement = db.select(Event)

    # Filter by category
    if category:
        statement = statement.where(
            Event.category == category
        )

    # Keyword search
    if search:
        search_pattern = f'%{search}%'

        statement = statement.where(
            or_(
                Event.title.ilike(search_pattern),
                Event.description.ilike(search_pattern),
                Event.venue.ilike(search_pattern)
            )
        )

    # Sort events by date and start time
    statement = statement.order_by(
        Event.date.asc(),
        Event.start_time.asc()
    )

    # Get events from database
    events = db.session.scalars(statement).all()

    # Get all available categories
    category_statement = (
        db.select(Event.category)
        .distinct()
        .order_by(Event.category)
    )

    categories = db.session.scalars(
        category_statement
    ).all()

    return render_template(
        'index.html',
        events=events,
        categories=categories,
        selected_category=category,
        search=search
    )


# TASK #12 - EVENT DETAILS PAGE
@main_bp.route('/event/<int:event_id>')
def event_details(event_id):
    # Find one event using its database ID
    event = db.get_or_404(Event, event_id)

    return render_template(
        'event.html',
        event=event
    )


# Create Event page
@main_bp.route('/create-event')
def create_event():
    return render_template('create_event.html')


# Booking History page
@main_bp.route('/history')
def history():
    return render_template('history.html')