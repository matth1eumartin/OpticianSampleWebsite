from flask_sqlalchemy import SQLAlchemy
import random 
import string 

db = SQLAlchemy()

def generateString():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=6))

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.String(6), default=generateString, unique=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(120), nullable=True)
    date = db.Column(db.String(8), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    location = db.Column(db.String(120), nullable=False)

class AvailableBookings(db.Model):
    __tablename__ = 'available_bookings'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(8), nullable=False)
    time = db.Column(db.String(5), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)

