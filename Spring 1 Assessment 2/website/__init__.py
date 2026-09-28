# Edited by Nulan
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    db.init_app(app)

    Bootstrap5(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id==user_id))

    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    # creates any missing tables in the database (User, Event, Comment, Order)
    with app.app_context():
        db.create_all()

    return app