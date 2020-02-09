import json
from random import sample

import click
from flask import Flask, redirect, render_template, request, session, url_for

from extensions import csrf, db, migrate, toolbar
from form import BookingForm, RequestForm
from models import Booking, Goal, Request, Tutor
from settings import BaseConfig as Config
from utilits import fill_db, format_phonenumber

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
toolbar.init_app(app)
csrf.init_app(app)
migrate.init_app(app, db, compare_type=True)


@app.cli.command()
def init():
    """Initialize database."""
    click.echo('Initializing the database...')
    db.create_all()


@app.cli.command()
def forge():
    """Generate tutors from json."""
    db.drop_all()
    db.create_all()
    click.echo('Initializing goals and tutors...')
    fill_db()


@app.route('/')
def index():
    all_goals = Goal.query.join(Goal.tutors).all()
    all_tutors = set()
    for goal in all_goals:
        all_tutors.update(goal.tutors)

    random_tutors = sample(all_tutors, 6)
    return render_template('index.html', goals=all_goals, tutors=random_tutors)


@app.route('/tutors/')
def fetch_tutors():
    all_goals = Goal.query.join(Goal.tutors).all()
    all_tutors = set()
    for goal in all_goals:
        all_tutors.update(goal.tutors)
    return render_template(
        'tutors.html',
        goals=all_goals,
        tutors=sorted(all_tutors, key=lambda tutor: tutor.uid),
    )


@app.route('/goals/<goal>/')
def goals(goal):
    user_goal = Goal.query.join(Goal.tutors).filter(Goal.name == goal).first_or_404()
    return render_template('goal.html', goal=user_goal, tutors=user_goal.tutors)


@app.route('/profiles/<int:tutor_id>/')
def tutors(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    tutor_schedule = json.loads(tutor.free)
    return render_template(
        'profile.html', tutor=tutor, goals=tutor.goals, schedule=tutor_schedule,
    )


@app.route('/request/', methods=['GET', 'POST'])
def send_request():
    form = RequestForm()
    if request.method == 'POST' and form.validate_on_submit():
        session['user_request'] = {
            'goal': form.data.get('goals'),
            'time': form.data.get('times'),
            'name': form.data.get('client_name'),
            'phone': form.data.get('client_phone'),
        }
        return redirect(url_for('sended_request'))

    return render_template('request.html', form=form)


@app.route('/request_done/')
def sended_request():
    if session.get('user_request') is None:
        return redirect(url_for('send_request'))
    user_request = session.pop('user_request')

    user_goal = Goal.query.filter_by(name=user_request['goal']).first_or_404()
    formatted_phone = format_phonenumber(user_request['phone'])

    user = Request(
        client_name=user_request['name'],
        client_phone=formatted_phone,
        client_time=user_request['time'],
        goal=user_goal,
    )
    db.session.add(user)
    db.session.commit()

    return render_template(
        'request_done.html',
        goal=user_goal.description,
        time=user_request['time'],
        name=user_request['name'],
        phone=formatted_phone,
    )


@app.route('/booking/<int:tutor_id>/', methods=['GET', 'POST'])
def book_tutor(tutor_id, day=None, time=None):
    weekdays = {
        'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота',
        'sun': 'Воскресенье',
    }
    client_day = request.args.get('day')
    schedule_day = weekdays[client_day]
    schedule_time = request.args.get('time')
    tutor = Tutor.query.get_or_404(tutor_id)
    form = BookingForm()

    if request.method == 'POST' and form.validate_on_submit():
        session['user_booking'] = {
            'tutor_id': tutor_id,
            'client_name': form.data.get('client_name'),
            'client_phone': form.data.get('client_phone'),
            'client_date': schedule_day,
            'client_time': schedule_time,
        }
        session['tutor_id'] = tutor_id
        session['client_name'] = form.data.get('client_name')
        session['client_phone'] = form.data.get('client_phone')
        session['client_date'] = schedule_day
        session['client_time'] = schedule_time
        return redirect(url_for('booking_done'))
    return render_template(
        'booking.html', form=form, tutor=tutor, day=client_day, time=schedule_time,
    )


@app.route('/booking_done/')
def booking_done():
    if session.get('user_booking') is None:
        return redirect(url_for('fetch_tutors'))
    user_booking = session.pop('user_booking')
    formatted_phone = format_phonenumber(user_booking['client_phone'])

    booking = Booking(
        tutor_id=user_booking['tutor_id'],
        client_name=user_booking['client_name'],
        client_phone=formatted_phone,
        client_date=user_booking['client_date'],
        client_time=user_booking['client_time'],
    )
    db.session.add(booking)
    db.session.commit()

    return render_template(
        'booking_done.html',
        name=user_booking['client_name'],
        phone=formatted_phone,
        day=user_booking['client_date'],
        time=user_booking['client_time'],
    )


if __name__ == '__main__':
    app.run()
