from website import create_app, db
from website.models import User, Event, Category
from datetime import datetime, timedelta
from flask_bcrypt import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    cat1 = Category(name='FPS')
    cat2 = Category(name='MOBA')
    cat3 = Category(name='RPG')
    cat4 = Category(name='Fighting')
    db.session.add_all([cat1, cat2, cat3, cat4])
    db.session.commit()

    hashed_pw = generate_password_hash('password123').decode('utf-8')
    user = User(
        first_name='Melvin',
        last_name='S',
        email='melvin@example.com',
        user_name='melvin',
        password_hash=hashed_pw,
        contact_number='1234567890',
        street_address='123 Main St'
    )
    db.session.add(user)
    db.session.commit()

    event1 = Event(
        title='FPS Tournament',
        description='A competitive first-person shooter tournament. Bring your best aim and reflexes!',
        date=datetime.now() + timedelta(days=30),
        location='Online',
        image_url='/static/img/fps.jpg',
        price=20.00,
        total_tickets=100,
        available_tickets=100,
        status='Open',
        creator_id=user.id,
        categories=[cat1]
    )

    event2 = Event(
        title='MOBA Cup',
        description='Team up with your squad for the ultimate MOBA championship. Strategy is key.',
        date=datetime.now() + timedelta(days=15),
        location='Online',
        image_url='/static/img/moba.jpg',
        price=15.00,
        total_tickets=50,
        available_tickets=50,
        status='Open',
        creator_id=user.id,
        categories=[cat2]
    )

    event3 = Event(
        title='RPG Night',
        description='A night of epic role-playing adventures. Join a party and defeat the final boss!',
        date=datetime.now() + timedelta(days=7),
        location='Sydney Game Center',
        image_url='/static/img/rpg.jpg',
        price=10.00,
        total_tickets=200,
        available_tickets=200,
        status='Open',
        creator_id=user.id,
        categories=[cat3]
    )

    event4 = Event(
        title='Fighting Championship',
        description='1v1 fighting game tournament. Prove you are the best in the scene.',
        date=datetime.now() + timedelta(days=45),
        location='Melbourne eSports Arena',
        image_url='/static/img/sample_event.jpg',
        price=25.00,
        total_tickets=64,
        available_tickets=64,
        status='Open',
        creator_id=user.id,
        categories=[cat4]
    )

    db.session.add_all([event1, event2, event3, event4])
    db.session.commit()

    print("Gaming Database seeded successfully!")
    print("Test User Login -> Username: melvin | Password: password123")
