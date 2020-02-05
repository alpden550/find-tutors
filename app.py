import json
from random import sample

import click
from flask import Flask, render_template, request

from extensions import csrf, db, migrate, toolbar
from form import BookingForm, RequestForm
from models import Booking, Goal, Request, Tutor
from settings import BaseConfig as Config
from utilits import fill_db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
toolbar.init_app(app)
csrf.init_app(app)
migrate.init_app(app, db)


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
        'tutors.html', goals=all_goals, tutors=sorted(all_tutors, key=lambda tutor: tutor.uid),
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


@app.route('/request/')
def send_request():
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/request_done/', methods=['POST'])
def sended_request():
    client_goal = request.form.get('goals')
    client_time = request.form.get('times')
    client_name = request.form.get('client_name')
    clinet_phone = request.form.get('client_phone')
    goal = Goal.query.filter_by(name=client_goal).first_or_404()

    user_request = Request(
        client_name=client_name,
        client_phone=clinet_phone,
        client_time=client_time,
        goal=goal,
    )
    db.session.add(user_request)
    db.session.commit()

    return render_template(
        'request_done.html',
        goal=goal.description,
        time=client_time,
        name=client_name,
        phone=clinet_phone,
    )


@app.route('/booking/<int:tutor_id>/')
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
    schedule_day = weekdays[request.args.get('day')]
    schedule_time = request.args.get('time')
    tutor = Tutor.query.get_or_404(tutor_id)
    form = BookingForm()
    form.client_day.default = schedule_day
    form.client_time.default = schedule_time
    form.tutor_id.default = tutor.uid
    form.process()
    return render_template(
        'booking.html', form=form, tutor=tutor,
    )


@app.route('/booking_done/', methods=['POST'])
def booking_done():
    client_name = request.form.get('client_name')
    client_phone = request.form.get('client_phone')
    client_day = request.form.get('client_day')
    client_time = request.form.get('client_time')
    tutor_id = request.form.get('tutor_id')

    booking = Booking(
        tutor_id=tutor_id,
        client_name=client_name,
        client_phone=client_phone,
        client_date=client_day,
        client_time=client_time,
    )
    db.session.add(booking)
    db.session.commit()

    return render_template(
        'booking_done.html',
        name=client_name,
        phone=client_phone,
        day=client_day,
        time=client_time,
    )


if __name__ == '__main__':
    app.run()
