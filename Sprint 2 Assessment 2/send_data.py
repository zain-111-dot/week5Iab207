from website import create_app, db
from website.models import User, Event, Category, Booking, Comment
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
    user1 = User(
        first_name='Melvin', last_name='S', email='melvin@example.com',
        user_name='melvin', password_hash=hashed_pw,
        contact_number='1234567890', street_address='123 Main St'
    )
    user2 = User(
        first_name='John', last_name='Doe', email='john@example.com',
        user_name='johndoe', password_hash=hashed_pw,
        contact_number='0987654321', street_address='456 Game St'
    )
    db.session.add_all([user1, user2])
    db.session.commit()

    event1 = Event(
        title='FPS Tournament', description='A competitive first-person shooter tournament. Bring your best aim!',
        date=datetime.now() + timedelta(days=30), location='Online', image_url='/static/img/fps.jpg',
        price=20.00, total_tickets=100, available_tickets=100, status='Open',
        creator_id=user1.id, categories=[cat1]
    )
    event2 = Event(
        title='MOBA Cup', description='Team up with your squad for the ultimate MOBA championship.',
        date=datetime.now() + timedelta(days=15), location='Online', image_url='/static/img/moba.jpg',
        price=15.00, total_tickets=50, available_tickets=50, status='Open',
        creator_id=user1.id, categories=[cat2]
    )
    event3 = Event(
        title='RPG Night', description='A night of epic role-playing adventures. Join a party!',
        date=datetime.now() + timedelta(days=7), location='Sydney Game Center', image_url='/static/img/rpg.jpg',
        price=10.00, total_tickets=200, available_tickets=200, status='Open',
        creator_id=user2.id, categories=[cat3]
    )
    db.session.add_all([event1, event2, event3])
    db.session.commit()

    booking1 = Booking(quantity=2, total_price=40.00, user_id=user1.id, event_id=event1.id)
    db.session.add(booking1)
    
    comment1 = Comment(content="Can't wait for this!", user_id=user2.id, event_id=event1.id)
    db.session.add(comment1)
    db.session.commit()

    print("Database seeded successfully!")
    print("User 1 -> Username: melvin | Password: password123")
    print("User 2 -> Username: johndoe | Password: password123")
