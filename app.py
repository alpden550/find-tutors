import json
from random import sample

import click
from flask import Flask, abort, render_template, request

from extensions import db, toolbar
from models import Goal, Tutor
from settings import BaseConfig as Config
from utilits import fetch_data_from_json, fetch_json, fill_db, write_json

NOT_FOUND_CODE = 404


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
toolbar.init_app(app)


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
    return render_template('request.html')


@app.route('/request_done/', methods=['POST'])
def sended_request(output_json='request.json'):
    all_goals = fetch_data_from_json('goals')
    client_goal = all_goals.get(request.form.get('goal'))
    client_time = request.form.get('time')
    client_name = request.form.get('client_name')
    clinet_phone = request.form.get('client_phone')

    all_requests = []
    all_requests.extend(fetch_json(json_file='request.json'))
    all_requests.append(
        {
            'client_name': client_name,
            'client_goal': client_goal,
            'client_time': client_time,
            'client_phone': clinet_phone,
        },
    )
    write_json(all_requests, output_json)

    return render_template(
        'request_done.html',
        goal=client_goal,
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
    all_tutors = fetch_data_from_json('teachers')
    try:
        tutor = next(tutor for tutor in all_tutors if tutor['id'] == tutor_id)
    except StopIteration:
        abort(NOT_FOUND_CODE, description='Resource not found')
    return render_template(
        'booking.html', tutor=tutor, day=schedule_day, time=schedule_time,
    )


@app.route('/booking_done/', methods=['POST'])
def booking_done(output_file='booking.json'):
    client_name = request.form.get('client_name')
    client_phone = request.form.get('client_phone')
    client_day = request.form.get('client_day')
    client_time = request.form.get('client_time')
    tutor_id = request.form.get('tutor_id')

    bookings = []
    bookings.extend(fetch_json(json_file='booking.json'))
    bookings.append(
        {
            'tutor_id': tutor_id,
            'client_name': client_name,
            'client_phone': client_phone,
            'client_day': client_day,
            'client_time': client_time,
        },
    )
    write_json(bookings, output_file)

    return render_template(
        'booking_done.html',
        name=client_name,
        phone=client_phone,
        day=client_day,
        time=client_time,
    )


if __name__ == '__main__':
    app.run()
