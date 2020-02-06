import json
from random import sample

import click
from flask import Flask, redirect, render_template, request, url_for

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
        context = {
            'goal': form.data.get('goals'),
            'time': form.data.get('times'),
            'name': form.data.get('client_name'),
            'phone': form.data.get('client_phone'),
        }
        return redirect(url_for('sended_request', context=json.dumps(context)))

    return render_template('request.html', form=form)


@app.route('/request_done/')
def sended_request(**kwargs):
    context = json.loads(request.args.get('context'))
    goal = context.get('goal')
    time = context.get('time')
    name = context.get('name')
    user_goal = Goal.query.filter_by(name=goal).first_or_404()
    formatted_phone = format_phonenumber(context.get('phone'))

    user_request = Request(
        client_name=name,
        client_phone=formatted_phone,
        client_time=time,
        goal=user_goal,
    )
    db.session.add(user_request)
    db.session.commit()

    return render_template(
        'request_done.html',
        goal=user_goal.description,
        time=time,
        name=name,
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
        client_name = form.data.get('client_name')
        client_phone = form.data.get('client_phone')
        return redirect(
            url_for(
                'booking_done',
                tutor_id=tutor_id,
                client_name=client_name,
                client_phone=client_phone,
                client_date=schedule_day,
                client_time=schedule_time,
            ),
        )
    return render_template(
        'booking.html', form=form, tutor=tutor, day=client_day, time=schedule_time,
    )


@app.route('/booking_done/')
def booking_done(**kwargs):
    client_name = request.args.get('client_name')
    client_day = request.args.get('client_date')
    client_time = request.args.get('client_time')
    tutor_id = request.args.get('tutor_id')
    formatted_phone = format_phonenumber(request.args.get('client_phone'))

    booking = Booking(
        tutor_id=tutor_id,
        client_name=client_name,
        client_phone=formatted_phone,
        client_date=client_day,
        client_time=client_time,
    )
    db.session.add(booking)
    db.session.commit()

    return render_template(
        'booking_done.html',
        name=client_name,
        phone=formatted_phone,
        day=client_day,
        time=client_time,
    )


if __name__ == '__main__':
    app.run()
