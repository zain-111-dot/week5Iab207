# Edited by Zain
from . import db
from datetime import datetime
from flask_login import UserMixin


# USER TABLE
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Used by the current login system
    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # Additional registration information required by Assignment 2
    first_name = db.Column(
        db.String(50),
        nullable=True
    )

    surname = db.Column(
        db.String(50),
        nullable=True
    )

    contact_number = db.Column(
        db.String(30),
        nullable=True
    )

    street_address = db.Column(
        db.String(200),
        nullable=True
    )

    # Relationships
    events = db.relationship(
        'Event',
        back_populates='creator'
    )

    comments = db.relationship(
        'Comment',
        back_populates='user'
    )

    bookings = db.relationship(
        'Order',
        back_populates='user'
    )


# EVENT TABLE
class Event(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(120),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False
    )

    start_time = db.Column(
        db.Time,
        nullable=False
    )

    end_time = db.Column(
        db.Time,
        nullable=False
    )

    venue = db.Column(
        db.String(150),
        nullable=False
    )

    image_url = db.Column(
        db.String(255),
        nullable=True
    )

    ticket_price = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    tickets_available = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Open, Inactive, Sold Out or Cancelled
    status = db.Column(
        db.String(20),
        nullable=False,
        default='Open'
    )

    # None, Generic or Enhanced
    acknowledgement = db.Column(
        db.String(20),
        nullable=False,
        default='None'
    )

    creator_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    creator = db.relationship(
        'User',
        back_populates='events'
    )

    comments = db.relationship(
        'Comment',
        back_populates='event'
    )

    bookings = db.relationship(
        'Order',
        back_populates='event'
    )


# COMMENT TABLE
class Comment(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('event.id'),
        nullable=False
    )

    user = db.relationship(
        'User',
        back_populates='comments'
    )

    event = db.relationship(
        'Event',
        back_populates='comments'
    )


# BOOKING TABLE
class Order(db.Model):
    __tablename__ = 'booking'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('event.id'),
        nullable=False
    )

    user = db.relationship(
        'User',
        back_populates='bookings'
    )

    event = db.relationship(
        'Event',
        back_populates='bookings'
    )
