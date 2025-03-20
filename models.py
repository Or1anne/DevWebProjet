from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # clé primiaire obligatoire pour SQLAlchemy
    email = db.Column(db.String(100), unique=True, index=True)
    pseudo = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100))
    lastname = db.Column(db.String(1000))
    firstname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(100))



