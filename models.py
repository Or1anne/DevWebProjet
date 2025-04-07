from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # clé primiaire obligatoire pour SQLAlchemy
    email = db.Column(db.String(100), unique=True, index=True)
    pseudo = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100))
    lastname = db.Column(db.String(1000))
    firstname = db.Column(db.String(100))
    level = db.Column(db.String, default="Debutant")
    role = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(100))
    point = db.Column(db.Integer, default=0)
    birthdate = db.Column(db.Date)
    image = db.Column(db.LargeBinary)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, unique=True, index=True)
    image = db.Column(db.LargeBinary)

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, unique=True, index=True)
    type = db.Column(db.String, nullable=False)
    reference = db.Column(db.String, unique=True, index=True)
    brand = db.Column(db.String)
    status = db.Column(db.String)
    image = db.Column(db.LargeBinary)

    battery = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    connectivity = db.Column(db.String)

    volume = db.Column(db.Integer)
    luminosity = db.Column(db.Integer)
    size = db.Column(db.Integer)
    resolution = db.Column(db.Integer)

    temp = db.Column(db.Integer)

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref=db.backref('objects', lazy=True))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    status = db.Column(db.String)

    object_name = db.Column(db.String)
    object_type = db.Column(db.String)

    user_lastname = db.Column(db.String)
    user_firstname = db.Column(db.String)
