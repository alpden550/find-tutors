from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/goals/<goal>/')
def goals(goal):
    return goal


@app.route('/profiles/<int:teacher_id>/')
def teachers(teacher_id):
    return 'Teacher %d' % teacher_id


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
