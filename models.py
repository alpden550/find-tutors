from extensions import db

goals_tutors = db.Table(
    'goals_tutors',
    db.Column('goal_id', db.Integer, db.ForeignKey('goal.uid'), primary_key=True),
    db.Column('tutor_id', db.Integer, db.ForeignKey('tutor.uid'), primary_key=True),
)


class Goal(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    tutors = db.relationship('Tutor', secondary=goals_tutors, back_populates='goals', lazy='joined')
    requests = db.relationship('Request', back_populates='goal', lazy='joining')

    def __repr__(self):
        return '<Goal {name}>'.format(name=self.name)


class Tutor(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    photo = db.Column(db.String(64))
    about = db.Column(db.Text)
    price = db.Column(db.Integer)
    rating = db.Column(db.Float)
    free = db.Column(db.Text)
    golas = db.relationship('Goal', secondary=goals_tutors, back_populates='tutors', lazy='joined')
    bookings = db.relationship('Booking', back_populates='tutor', lazy='joined')

    def __repr__(self):
        return '<Tutor {name}>'.format(name=self.name)


class Booking(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.uid'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Booking {uid}>'.format(uid=self.uid)


class Request(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(20), nullable=False)
    client_phone = db.Column(db.Integer, nullable=False)
    client_time = db.Column(db.String(10), nullable=False)
    client_goal = db.Column(db.Integer, db.ForeignKey('goal.uid'), nullable=False)

    def __repr__(self):
        return '<Request {uid}>'.format(uid=self.uid)
