from website import create_app, db
from website.models import User, Event, Category, Order, Comment
from datetime import datetime, timedelta
from flask_bcrypt import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create Categories
    cat1 = Category(name='FPS')
    cat2 = Category(name='MOBA')
    cat3 = Category(name='RPG')
    cat4 = Category(name='Fighting')
    db.session.add_all([cat1, cat2, cat3, cat4])
    db.session.commit()

    # Create a Test User
    hashed_pw = generate_password_hash('password123').decode('utf-8')
    user = User(
        first_name='Melvin',
        surname='S',
        email='melvin@example.com',
        name='melvin',
        password_hash=hashed_pw,
        contact_number='1234567890',
        street_address='123 Main St'
    )
    db.session.add(user)
    db.session.commit()

    # Create Events
    event1 = Event(
        title='FPS Tournament', description='A competitive first-person shooter tournament. Bring your best aim!',
        date=datetime.now() + timedelta(days=30), start_time=datetime.now().time(), end_time=(datetime.now() + timedelta(hours=4)).time(),
        venue='Online', image_url='/static/img/fps.jpg', ticket_price=20.00, tickets_available=100,
        status='Open', acknowledgement='None', creator_id=user.id, category='FPS'
    )
    event2 = Event(
        title='MOBA Cup', description='Team up with your squad for the ultimate MOBA championship.',
        date=datetime.now() + timedelta(days=15), start_time=datetime.now().time(), end_time=(datetime.now() + timedelta(hours=3)).time(),
        venue='Online', image_url='/static/img/moba.jpg', ticket_price=15.00, tickets_available=50,
        status='Open', acknowledgement='None', creator_id=user.id, category='MOBA'
    )
    event3 = Event(
        title='RPG Night', description='A night of epic role-playing adventures. Join a party!',
        date=datetime.now() + timedelta(days=7), start_time=datetime.now().time(), end_time=(datetime.now() + timedelta(hours=5)).time(),
        venue='Sydney Game Center', image_url='/static/img/rpg.jpg', ticket_price=10.00, tickets_available=200,
        status='Open', acknowledgement='None', creator_id=user.id, category='RPG'
    )
    event4 = Event(
        title='Fighting Championship', description='1v1 fighting game tournament. Prove you are the best in the scene.',
        date=datetime.now() + timedelta(days=45), start_time=datetime.now().time(), end_time=(datetime.now() + timedelta(hours=6)).time(),
        venue='Melbourne eSports Arena', image_url='/static/img/sample_event.jpg', ticket_price=25.00, tickets_available=64,
        status='Open', acknowledgement='None', creator_id=user.id, category='Fighting'
    )

    db.session.add_all([event1, event2, event3, event4])
    db.session.commit()

    # Create Booking (Order) and Comment
    order1 = Order(price=40.00, quantity=2, user_id=user.id, event_id=event1.id)
    comment1 = Comment(text="Can't wait for this!", user_id=user.id, event_id=event1.id)
    db.session.add(order1)
    db.session.add(comment1)
    db.session.commit()

    print("Database seeded successfully!")
    print("Test User Login -> Username: melvin | Password: password123")