import json
from pathlib import Path

from flask import Flask, render_template, abort

app = Flask(__name__)

TUTORS_JSON = 'tutors.json'
NOT_FOUND_CODE = 404

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
        abort(NOT_FOUND_CODE, description="Resource not found")
    tutor_goals = [all_goals[goal] for goal in tutor['goals']]

    return render_template('profile.html', tutor=tutor, goals=tutor_goals)


@app.route('/request/')
def send_request():
    return 'request'


@app.route('/request_done/')
def sended_request():
    return 'request_done'


@app.route('/booking/<int:teacher_id>/')
def book_teacher(teacher_id):
    return 'Teacher %d' % teacher_id


@app.route('/booking_done/')
def booking_done():
    return 'booking_done'


if __name__ == '__main__':
    app.run()
