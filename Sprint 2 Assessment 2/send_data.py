from website import create_app, db
from website.models import User, Event, Category, Order, Comment
from datetime import datetime, timedelta, time
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

    # Create Test Users
    hashed_pw = generate_password_hash('password123').decode('utf-8')
    user1 = User(
        first_name='Melvin', surname='S', email='melvin@example.com',
        name='melvin', password_hash=hashed_pw,
        contact_number='1234567890', street_address='123 Main St'
    )
    user2 = User(
        first_name='John', surname='Doe', email='john@example.com',
        name='johndoe', password_hash=hashed_pw,
        contact_number='0987654321', street_address='456 Game St'
    )
    db.session.add_all([user1, user2])
    db.session.commit()

    # Create Events (Fixed times)
    event1 = Event(
        title='FPS Tournament', description='A competitive first-person shooter tournament. Bring your best aim!',
        date=datetime.now().date() + timedelta(days=30), start_time=time(18, 0), end_time=time(22, 0),
        venue='Online', image_url='/static/img/fps.jpg', ticket_price=20.00, tickets_available=100,
        status='Open', acknowledgement='None', creator_id=user1.id, category='FPS'
    )
    event2 = Event(
        title='MOBA Cup', description='Team up with your squad for the ultimate MOBA championship.',
        date=datetime.now().date() + timedelta(days=15), start_time=time(19, 30), end_time=time(22, 30),
        venue='Online', image_url='/static/img/moba.jpg', ticket_price=15.00, tickets_available=50,
        status='Open', acknowledgement='None', creator_id=user1.id, category='MOBA'
    )
    event3 = Event(
        title='RPG Night', description='A night of epic role-playing adventures. Join a party!',
        date=datetime.now().date() + timedelta(days=7), start_time=time(17, 0), end_time=time(23, 0),
        venue='Sydney Game Center', image_url='/static/img/rpg.jpg', ticket_price=10.00, tickets_available=200,
        status='Open', acknowledgement='None', creator_id=user2.id, category='RPG'
    )

    db.session.add_all([event1, event2, event3])
    db.session.commit()

    # Create Bookings (Orders)
    order1 = Order(price=40.00, quantity=2, user_id=user1.id, event_id=event1.id)
    order2 = Order(price=15.00, quantity=1, user_id=user2.id, event_id=event2.id)
    db.session.add_all([order1, order2])
    
    # Create Comments
    comment1 = Comment(text="Can't wait for this tournament!", user_id=user2.id, event_id=event1.id)
    comment2 = Comment(text="Is there a prize pool?", user_id=user1.id, event_id=event1.id)
    db.session.add_all([comment1, comment2])
    
    db.session.commit()

    print("Gaming Database seeded successfully!")
    print("User 1 -> Username: melvin | Password: password123")
    print("User 2 -> Username: johndoe | Password: password123")
