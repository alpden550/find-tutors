import json
from pathlib import Path

from flask import Flask, abort, render_template, request

app = Flask(__name__)

TUTORS_JSON = 'tutors.json'
NOT_FOUND_CODE = 404


def fetch_json(json_file='booking.json'):
    try:
        return json.loads(Path(json_file).read_text())
    except FileNotFoundError:
        return []


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/goals/<goal>/')
def goals(goal):
    return goal


@app.route('/profiles/<int:tutor_id>/')
def tutors(tutor_id):
    tutors_data = json.loads(Path(TUTORS_JSON).read_text())
    all_goals = tutors_data.get('goals')
    all_tutors = tutors_data.get('teachers')
    try:
        tutor = next(tutor for tutor in all_tutors if tutor['id'] == tutor_id)
    except StopIteration:
        abort(NOT_FOUND_CODE, description='Resource not found')
    tutor_goals = [all_goals[goal] for goal in tutor['goals']]

    return render_template('profile.html', tutor=tutor, goals=tutor_goals)


@app.route('/request/')
def send_request():
    return render_template('request.html')


@app.route('/request_done/')
def sended_request():
    return 'request_done'


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
    all_tutors = json.loads(Path(TUTORS_JSON).read_text()).get('teachers')
    try:
        tutor = next(tutor for tutor in all_tutors if tutor['id'] == tutor_id)
    except StopIteration:
        abort(NOT_FOUND_CODE, description='Resource not found')
    return render_template(
        'booking.html', tutor=tutor, day=schedule_day, time=schedule_time
    )


@app.route('/booking_done/', methods=['POST'])
def booking_done(output_file='booking.json'):
    client_name = request.form.get('client_name')
    client_phone = request.form.get('client_phone')
    client_day = request.form.get('client_day')
    client_time = request.form.get('client_time')
    tutor_id = request.form.get('tutor_id')

    bookings = []
    bookings.extend(fetch_json())
    bookings.append(
        {
            'tutor_id': tutor_id,
            'client_name': client_name,
            'client_phone': client_phone,
            'client_day': client_day,
            'client_time': client_time,
        },
    )

    with open(output_file, 'w+') as json_handler:
        json.dump(
            bookings,
            json_handler,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )

    return render_template(
        'booking_done.html',
        name=client_name,
        phone=client_phone,
        day=client_day,
        time=client_time,
    )


if __name__ == '__main__':
    app.run()
