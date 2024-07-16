from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from .models import RegisteredUser, Stadium, Tournament, Match, Ticket, Seat
from . import db
import os
import secrets
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    matches = Match.query.all()
    tournaments = Tournament.query.all()
    
    return render_template('home.html', user = current_user, tournaments = tournaments)

@views.route('/tournaments')
@login_required
def tournaments():
    if current_user.is_tournament_admin == True:
        return render_template('tournaments.html', user = current_user)
    return redirect(url_for('views.home'))

@views.route('/add_tournaments', methods=['GET', 'POST'])
@login_required
def add_tournaments():
    print(f"### current_user.is_super_admin {current_user.is_super_admin}")
    if current_user.is_tournament_admin == True:
        if request.method == 'POST':
            tournament_title =  request.form.get('title')
            tournament_starring = request.form.get('starring')
            tournament_production_house = request.form.get('organizer')
            tournament_no_of_watched = 0
            print(type(request.files['poster']))
            tournament_poster = save_images(request.files['poster'])

            # check if all the fields are not empty
            print(f'#####: tournament_title: {tournament_title}')
            print(f'#####: tournament_production_house: {tournament_production_house}')
            print(f'#####: tournament_starring: {tournament_starring}')
            if len(tournament_title) >= 1 and len(tournament_starring) >= 1 and len(tournament_production_house) >= 1 :
                # good to go
                new_tournament = Tournament(poster = tournament_poster, title = tournament_title, starring = tournament_starring, organizer = tournament_production_house, no_of_watched = tournament_no_of_watched, tournament_admin_id = current_user.id)

                db.session.add(new_tournament)
                db.session.commit()

                flash( tournament_title + ' is being added', category='success')
                return redirect(url_for('views.tournaments'))
            else:
                flash('Make sure all the fields are filled', category='error')
                return render_template('add_tournaments.html', user = current_user)
        else:
            return render_template('add_tournaments.html', user = current_user)
    return redirect(url_for('views.home'))


@views.route('/update_tournaments/<int:id>', methods = ['POST', 'GET'])
@login_required
def update_tournaments(id):
    if current_user.is_super_admin == True or current_user.is_tournament_admin:
        tournament_to_update = Tournament.query.get(int(id))
        if request.method == 'POST':
            tournament_to_update.poster = save_images(request.files['poster'])
            tournament_to_update.title =  request.form.get('title')
            tournament_to_update.starring = request.form.get('starring')
            tournament_to_update.organizer = request.form.get('organizer')
            
            db.session.commit()

            flash( tournament_to_update.title + ' updated succesfully', category='success')
            return redirect(url_for('views.tournaments'))
        else:
            if tournament_to_update:
                return render_template('update_tournaments.html', user = current_user, tournament = tournament_to_update)
    else:
        return redirect(url_for('tournaments.home'))



@views.route('/my_stadiums')
@login_required
def my_stadiums():
    print(f"#####is_super_admin: {current_user.is_super_admin}")
    if current_user.is_super_admin == True:
        tournaments = Tournament.query.all()
        return render_template('my_stadiums.html', user = current_user, tournaments = tournaments)
    return redirect(url_for('views.home'))

@views.route('/select_stadiums/<int:id>')
def select_stadiums(id):
    # tournament_id
    matches = Match.query.filter_by(tournament_screened = int(id)).all()
    tournament = Tournament.query.get(int(id))
    print("line 90")
    if matches:
        return render_template('select_stadiums.html', user = current_user, matches = matches, tournament = tournament)
    else :
        flash( 'This tournament has no matches currently', category='note')
        return redirect(url_for('views.home'))

@views.route('/add_stadiums', methods=['GET', 'POST'])
@login_required
def add_stadiums():
    if current_user.is_super_admin == True:
        if request.method == 'POST':
            stadium_name =  request.form.get('name')
            stadium_address = request.form.get('address')
            stadium_location = request.form.get('location')
            stadium_city = request.form.get('city')
            stadium_contact_no = request.form.get('contact_no')

            # check if all the fields are not empty
            if len(stadium_name) >= 1 and len(stadium_address) >= 1 and len(stadium_location) >= 1 and len(stadium_city) >= 1 and len(stadium_contact_no) == 10:
                # good to go
                new_stadium = Stadium(name = stadium_name, address = stadium_address, location = stadium_location, city = stadium_city, contact_no = stadium_contact_no, stadium_admin_id = current_user.id)
                db.session.add(new_stadium)
                db.session.commit()

                flash('Your Stadium is being added', category='success')
                return redirect(url_for('views.my_stadiums'))
            else:
                flash('Make sure all the fields are filled', category='error')
                return render_template('add_stadiums.html', user = current_user)
        else:
            return render_template('add_stadiums.html', user = current_user)
    return redirect(url_for('views.home'))

@views.route('/my_tickets')
@login_required
def my_tickets():
    return render_template('my_tickets.html', user = current_user)

@views.route('/book_ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def book_ticket(id):
    if current_user.is_super_admin == False and current_user.is_tournament_admin == False:
        match_to_book = Match.query.get(int(id))
        seats = Seat.query.filter_by(match_id=id).all()
        if request.method == 'POST':
            selected_seat_ids = request.form.getlist('selected_seats')[0].split(',')
            selected_seat_count = len(selected_seat_ids)
            if (selected_seat_count == 1 and selected_seat_ids[0] == '') \
                or \
               (selected_seat_count > 0 and selected_seat_count <= match_to_book.seats_available):
                match_to_book.seats_available -= selected_seat_count
                for seat_id in selected_seat_ids:
                    seat = Seat.query.get(int(seat_id))
                    seat.is_available = False
                
                new_ticket = Ticket(
                    match_booked=match_to_book.id,
                    tournament_booked=match_to_book.tournament_screened,
                    stadium_booked=match_to_book.stadium_screened_in,
                    user=current_user.id,
                    tournament_name=match_to_book.tournament,
                    stadium_name=match_to_book.stadium,
                    stadium_address=match_to_book.stadium_address,
                    stadium_address_link=match_to_book.stadium_address_link,
                    no_of_seats=selected_seat_count,
                    total_cost=int(match_to_book.cost_per_seat) * selected_seat_count,
                    match_timinig=match_to_book.datetime_screened
                )
                
                db.session.add(new_ticket)
                db.session.commit()
                flash('Your ticket has been booked successfully', category='success')
                return redirect(url_for('views.my_tickets'))
            else:
                flash('Selected seats are not available', category='error')
                return render_template('book_ticket.html', user=current_user, match=match_to_book, seats=seats)
        else:
            return render_template('book_ticket.html', user=current_user, match=match_to_book, seats=seats)
    else:
        return redirect(url_for('views.home'))


@views.route('/add_matches', methods=['GET', 'POST'])
@login_required
def add_matches():
    tournaments = Tournament.query.all()
    stadium = Stadium.query.filter_by(stadium_admin_id=int(current_user.id)).all()
    if current_user.is_super_admin == True:
        if request.method == 'POST':
            match_tournament_screened = Tournament.query.filter_by(title=request.form.get('tournament_screened')).first().id
            if match_tournament_screened:
                match_stadium_screened_in = int(request.form.get('stadium_screened_in'))
                match_tournament = request.form.get('tournament_screened')
                match_stadium = Stadium.query.filter_by(id=request.form.get('stadium_screened_in')).first()
                match_date_time_screened = datetime.strptime(request.form.get('date_time_screened'), '%Y-%m-%dT%H:%M')
                match_seats_available = int(request.form.get('seats_available'))
                match_cost_per_seat = request.form.get('cost_per_seat')
            else:
                flash('Tournament doesn\'t exist', category='warning')
                return render_template('add_matches.html', user=current_user, tournaments=tournaments, stadium=stadium)
            
            if match_tournament_screened >= 1 and match_stadium_screened_in >= 1 and match_seats_available >= 1:
                new_match = Match(
                    tournament_screened=match_tournament_screened,
                    stadium_screened_in=match_stadium_screened_in,
                    tournament=match_tournament,
                    stadium=match_stadium.name,
                    stadium_address=match_stadium.address,
                    stadium_address_link=match_stadium.location,
                    datetime_screened=match_date_time_screened,
                    stadium_admin_id=current_user.id,
                    seats_available=match_seats_available,
                    cost_per_seat=match_cost_per_seat
                )
                db.session.add(new_match)
                db.session.commit()

                # Seed seats
                for seat_num in range(1, match_seats_available + 1):
                    seat = Seat(match_id=new_match.id, seat_number=f'S{seat_num}', is_available=True)
                    db.session.add(seat)

                db.session.commit()
                flash('Your Match is being added', category='success')
                return redirect(url_for('views.my_stadiums'))
            else:
                flash('Make sure all the fields are filled', category='error')
                return render_template('add_matches.html', user=current_user, tournaments=tournaments, stadium=stadium)
        else:
            return render_template('add_matches.html', user=current_user, tournaments=tournaments, stadium=stadium)
    else:
        return render_template('home.html', user=current_user, tournaments=tournaments)


@views.route('match_tickets/<int:id>')
@login_required
def match_tickets(id):
    if current_user.is_tournament_admin == True:
        tickets = Ticket.query.filter_by(match_booked = int(id)).all()
        match = Match.query.get(int(id))
        return render_template('match_tickets.html', user = current_user, tickets = tickets, match = match, no_of_tickets = len(tickets))
    else:
        return render_template('home.html', user = current_user, tournaments = tournaments)
        

def save_images(poster):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(poster.filename)
    image_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/tournament_posters', image_name)
    poster.save(file_path)
    return image_name

