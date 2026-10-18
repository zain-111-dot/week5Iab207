# Edited by Zain

from sqlalchemy import or_
from sentence_transformers import SentenceTransformer, util
from . import db
from .models import Event

semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
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
    query = (query or '').strip()

    if not query:
        return []

    events = db.session.scalars(db.select(Event)).all()

    if not events:
        return []

    event_texts = [
        f"{event.title or ''} "
        f"{event.category or ''} "
        f"{event.description or ''} "
        f"{event.venue or ''}"
        for event in events
    ]

    query_embedding = semantic_model.encode(
        query,
        convert_to_tensor=True
    )

    event_embeddings = semantic_model.encode(
        event_texts,
        convert_to_tensor=True
    )

    similarity_scores = util.cos_sim(
        query_embedding,
        event_embeddings
    )[0]

    ranked_results = sorted(
        zip(similarity_scores.tolist(), events),
        key=lambda result: result[0],
        reverse=True
    )

    return [
        event
        for score, event in ranked_results
        if score >= 0.25
    ]

    
    
    