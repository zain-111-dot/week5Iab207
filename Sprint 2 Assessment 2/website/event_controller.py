# Edited by Zain
from sqlalchemy import or_

from . import db
from .models import Event


def get_events(search='', category=''):
    statement = db.select(Event)

    if category:
        statement = statement.where(
            Event.category == category
        )

    if search:
        search_pattern = f'%{search}%'

        statement = statement.where(
            or_(
                Event.title.ilike(search_pattern),
                Event.description.ilike(search_pattern),
                Event.venue.ilike(search_pattern)
            )
        )

    statement = statement.order_by(
        Event.date.asc(),
        Event.start_time.asc()
    )

    events = db.session.scalars(statement).all()

    for event in events:
        event.update_status()

    db.session.commit()

    return events


def get_categories():
    statement = (
        db.select(Event.category)
        .distinct()
        .order_by(Event.category)
    )

    return db.session.scalars(statement).all()


def get_event(event_id):
    event = db.get_or_404(Event, event_id)

    old_status = event.status
    event.update_status()

    if event.status != old_status:
        db.session.commit()

    return event
def semantic_search(query):
    query = query.lower().strip()

    if not query:
        return []

    # Related gaming terms used for semantic-style matching
    related_terms = {
        'shooter': ['fps', 'shooting', 'tournament', 'competition'],
        'fps': ['shooter', 'shooting', 'tournament'],
        'role playing': ['rpg', 'adventure', 'roleplay'],
        'rpg': ['role playing', 'roleplay', 'adventure'],
        'fighting': ['fighter', 'championship', 'combat'],
        'fighter': ['fighting', 'championship', 'combat'],
        'strategy': ['moba', 'team', 'competition'],
        'moba': ['strategy', 'team', 'competition'],
        'online': ['virtual', 'internet'],
        'competition': ['tournament', 'championship']
    }

    search_words = set(query.split())

    for word, related in related_terms.items():
        if word in query:
            search_words.update(related)

    events = db.session.scalars(
        db.select(Event).order_by(
            Event.date.asc(),
            Event.start_time.asc()
        )
    ).all()

    matched_events = []

    for event in events:
        event_text = (
            f'{event.title} '
            f'{event.category} '
            f'{event.description} '
            f'{event.venue}'
        ).lower()

        score = 0

        for word in search_words:
            if word in event_text:
                score += 1

        if score > 0:
            matched_events.append((score, event))

    matched_events.sort(
        key=lambda result: result[0],
        reverse=True
    )

    return [event for score, event in matched_events]