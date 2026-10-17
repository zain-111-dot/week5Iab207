# Edited by Zain
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from flask_login import current_user, login_required
from . import db
from .models import Event, Category, Order, Comment
from .forms import EventForm, BookingForm, CommentForm
from .event_controller import get_events, get_categories, get_event, semantic_search
from datetime import datetime

# Main website routes
main_bp = Blueprint('views', __name__)

# TASK #11 - LANDING PAGE AND EVENT LISTING
@main_bp.route('/')
def index():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    events = get_events(search=search, category=category)
    categories = get_categories()

    for event in events:
        event.update_status()

    db.session.commit()

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
    event.update_status()
    db.session.commit()
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_posted.desc()).all()
    return render_template(
        'event_detail.html',
        event=event,
        booking_form=BookingForm(),
        comment_form=CommentForm(),
        comments=comments
    )

# Create Event page (Moved to Sprint 1)
@main_bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            category=form.category.data,
            description=form.description.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            venue=form.venue.data,
            image_url=form.image_url.data,
            ticket_price=form.ticket_price.data,
            tickets_available=form.tickets_available.data,
            acknowledgement=form.acknowledgement.data,
            acknowledgement_text=form.acknowledgement_text.data,
            creator_id=current_user.id,
            status='Open'
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('views.event_details', event_id=event.id))
    return render_template('create_event.html', form=form)

# Edit Event page
@main_bp.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = db.get_or_404(Event, event_id)
    if event.creator_id != current_user.id:
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('views.event_details', event_id=event.id))
    
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.category = form.category.data
        event.description = form.description.data
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.venue = form.venue.data
        event.image_url = form.image_url.data
        event.ticket_price = form.ticket_price.data
        event.tickets_available = form.tickets_available.data
        event.acknowledgement = form.acknowledgement.data
        event.acknowledgement_text = form.acknowledgement_text.data
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('views.event_details', event_id=event.id))
    return render_template('create_event.html', form=form, event=event)

# Cancel Event
@main_bp.route('/cancel-event/<int:event_id>', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = db.get_or_404(Event, event_id)
    if event.creator_id != current_user.id:
        flash('You do not have permission to cancel this event.', 'danger')
        return redirect(url_for('views.event_details', event_id=event.id))
    event.status = 'Cancelled'
    db.session.commit()
    flash('Event cancelled successfully.', 'success')
    return redirect(url_for('views.event_details', event_id=event.id))

# My Events page
@main_bp.route('/my-events')
@login_required
def my_events():
    events = Event.query.filter_by(creator_id=current_user.id).order_by(Event.date.desc()).all()
    return render_template('my_events.html', events=events)

# Book Tickets
@main_bp.route('/book/<int:event_id>', methods=['POST'])
@login_required
def book_event(event_id):
    event = db.get_or_404(Event, event_id)
    form = BookingForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        if quantity > event.tickets_available:
            flash(f'Only {event.tickets_available} tickets available.', 'danger')
            return redirect(url_for('views.event_details', event_id=event.id))
        
        order = Order(price=event.ticket_price * quantity, quantity=quantity, user_id=current_user.id, event_id=event.id)
        event.tickets_available -= quantity
        if event.tickets_available <= 0:
            event.status = 'Sold Out'
        db.session.add(order)
        db.session.commit()
        flash(f'Booking successful! Order ID: {order.id}', 'success')
        return redirect(url_for('views.history'))
    return redirect(url_for('views.event_details', event_id=event.id))

# Post Comment
@main_bp.route('/comment/<int:event_id>', methods=['POST'])
@login_required
def add_comment(event_id):
    event = db.get_or_404(Event, event_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, user_id=current_user.id, event_id=event.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!', 'success')
    return redirect(url_for('views.event_details', event_id=event.id))

# Booking History page
@main_bp.route('/history')
@login_required
def history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.booking_date.desc()).all()
    return render_template('history.html', orders=orders)

# Acknowledgement of Country page
@main_bp.route('/acknowledgement')
def acknowledgement():
    return render_template('acknowledgement.html')
# SEARCH RESULTS PAGE
@main_bp.route('/search')
def search_results():
    query = request.args.get('search', '').strip()

    traditional_results = get_events(search=query)
    ai_results = semantic_search(query)

    return render_template(
        'search_results.html',
        search_query=query,
        traditional_results=traditional_results,
        ai_results=ai_results
    )


# TO TEST 500 ERROR PAGE
@main_bp.route('/test-500')
def test_500():
    return 1 / 0
