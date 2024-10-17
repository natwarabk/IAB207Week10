from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    # Password is never stored in the DB in plain text; an encrypted password is stored
    # The storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # Relation to call user.comments and comment.name
    comments = db.relationship('Comment', backref='user')

    # String print method
    def __repr__(self):
        return f"Name: {self.name}"

class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(3))
    # Create the Comments db.relationship
    # Relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='destination')

    # String print method
    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # Add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

    # String print method
    def __repr__(self):
        return f"Comment: {self.text}"
