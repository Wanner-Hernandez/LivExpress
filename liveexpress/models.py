from liveexpress import db
from liveexpress import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(70), nullable=False)
    lname = db.Column(db.String(70), nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User({self.username})\tIs Admin: {self.is_admin}"

class GuestUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"User({self.id})"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hashtags = db.Column(db.String)
    image_file = db.Column(db.String(100), nullable=False, default='blog-default.jpg')


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"