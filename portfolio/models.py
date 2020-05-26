#MODELS
#from portfolio import db
from werkzeug.security import generate_password_hash, check_password_hash
#from portfolio import login_manager
from flask_login import UserMixin
from portfolio.extensions import db
from portfolio.extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Essay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return self.title


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    image = db.Column(db.Text)
    def __init__(self, title, description, image):
        self.title = title
        self.description = description
        self.image = image

    def __repr__(self):
        return self.title
