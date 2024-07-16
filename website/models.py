from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class RegisteredUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    is_tournament_admin = db.Column(db.Boolean)
    is_super_admin = db.Column(db.Boolean)
    stadium = db.relationship('Stadium')
    tournaments = db.relationship('Tournament')
    matches = db.relationship('Match')
    tickets_booked = db.relationship('Ticket')

class Stadium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    location = db.Column(db.String(150))
    city =  db.Column(db.String(150))
    contact_no = db.Column(db.String(10))
    stadium_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    matches = db.relationship('Match')
    tickets_booked = db.relationship('Ticket')

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.String(255))
    title = db.Column(db.String(150))
    starring = db.Column(db.String(250))
    organizer = db.Column(db.String(150))
    no_of_watched =  db.Column(db.Integer)
    tournament_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    matches = db.relationship('Match')
    tickets_booked = db.relationship('Ticket')

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_screened = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    stadium_screened_in = db.Column(db.Integer, db.ForeignKey('stadium.id'))
    tournament = db.Column(db.String(150))
    stadium = db.Column(db.String(150))
    stadium_address = db.Column(db.String(150))
    stadium_address_link = db.Column(db.String(150))
    datetime_screened = db.Column(db.DateTime(timezone=True), default=func.now())
    stadium_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    seats_available = db.Column(db.Integer)
    cost_per_seat = db.Column(db.Integer)
    seats = db.relationship('Seat', back_populates='match', lazy=True)
    tickets_booked = db.relationship('Ticket')

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    match = db.relationship('Match', back_populates='seats')


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_booked = db.Column(db.Integer, db.ForeignKey('match.id'))
    tournament_booked = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    stadium_booked = db.Column(db.Integer, db.ForeignKey('stadium.id'))
    user = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    tournament_name = db.Column(db.String(150))
    stadium_name = db.Column(db.String(150))
    stadium_address = db.Column(db.String(150))
    stadium_address_link = db.Column(db.String(150))
    no_of_seats = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)
    match_timinig = db.Column(db.DateTime(timezone=True), default=func.now())

