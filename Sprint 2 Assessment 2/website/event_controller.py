# Edited by Zain

from sqlalchemy import or_

from . import db
from .models import Event


def get_events(search='', category=''):
    """Retrieve events using optional keyword and category filters."""

    statement = db.select(Event)

    if category:
        statement = statement.where(Event.category == category)

    if search:
        search_pattern = f'%{search}%'

        statement = statement.where(
            or_(
                Event.title.ilike(search_pattern),
                Event.category.ilike(search_pattern),
                Event.description.ilike(search_pattern),
                Event.venue.ilike(search_pattern)
            )
        )

    statement = statement.order_by(
        Event.date.asc(),
        Event.start_time.asc()
    )

    return db.session.scalars(statement).all()


def get_categories():
    """Return the different event categories."""

    statement = (
        db.select(Event.category)
        .distinct()
        .order_by(Event.category)
    )

    return db.session.scalars(statement).all()


def get_event(event_id):
    """Retrieve one event using its database ID."""

    return db.get_or_404(Event, event_id)


def semantic_search(query):
    """Find events using related gaming concepts as well as exact words."""

    query = (query or '').strip().lower()

    if not query:
        return []

    events = db.session.scalars(db.select(Event)).all()

    related_words = {
        'strategy': ['moba', 'rpg', 'team', 'championship'],
        'team': ['moba', 'fps', 'squad', 'competition'],
        'shooter': ['fps', 'shooting', 'tournament'],
        'combat': ['fighting', 'fps', 'battle'],
        'role': ['rpg', 'adventure', 'role-playing'],
        'competitive': ['competition', 'tournament', 'fps', 'moba'],
        'tournament': ['competition', 'championship', 'fps', 'moba'],
    }

    search_words = query.split()
    expanded_words = set(search_words)

    for word in search_words:
        expanded_words.update(related_words.get(word, []))

    matched_events = []

    for event in events:
        event_text = (
            f'{event.title} '
            f'{event.category} '
            f'{event.description} '
            f'{event.venue}'
        ).lower()

        score = 0

        for word in expanded_words:
            if word in event_text:
                score += 1

        if score > 0:
            matched_events.append((score, event))

    matched_events.sort(
        key=lambda result: result[0],
        reverse=True
    )

    return [event for score, event in matched_events]
