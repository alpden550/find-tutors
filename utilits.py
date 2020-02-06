import json
from pathlib import Path

import click
import phonenumbers
from sqlalchemy.exc import IntegrityError

import models
from extensions import db

TUTORS_JSON = 'tutors.json'


def fetch_json(json_file):
    try:
        return json.loads(Path(json_file).read_text())
    except FileNotFoundError:
        return []


def write_json(json_data, output):
    with open(output, 'w+') as json_handler:
        json.dump(
            json_data,
            json_handler,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )


def fetch_data_from_json(fetched, json_file=TUTORS_JSON):
    return json.loads(Path(json_file).read_text()).get(fetched)


def create_goals(goals):
    for name, description in goals.items():
        goal = models.Goal(name=name, description=description)
        db.session.add(goal)
        try:  # noqa:WPS229
            db.session.commit()
            click.echo('Added goal {goal}'.format(goal=goal))
        except IntegrityError:
            db.session.rollback()


def create_tutors(tutors):
    for person in tutors:
        shedule = json.dumps(person['free'])
        tutor = models.Tutor(
            name=person.get('name'),
            photo=person.get('picture'),
            about=person.get('about'),
            price=person.get('price'),
            rating=person.get('rating'),
            free=shedule,
        )
        db.session.add(tutor)

        for name in person['goals']:
            goal = models.Goal.query.filter_by(name=name).first()
            goal.tutors.append(tutor)
            click.echo('Added goals {goals} for {tutor}'.format(goals=goal, tutor=tutor))
        try:  # noqa:WPS229
            db.session.commit()
            click.echo('Added tutor {tutor}'.format(tutor=tutor))
        except IntegrityError:
            db.session.rollback()


def fill_db(input_json=TUTORS_JSON):
    goals = fetch_data_from_json('goals')
    tutors = fetch_data_from_json('teachers')
    create_goals(goals)
    create_tutors(tutors)


def format_phonenumber(phonenumber, code='RU'):
    phone = phonenumbers.parse(phonenumber, 'RU')
    return phonenumbers.format_number(
        phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL,
    )


if __name__ == '__main__':
    fill_db()
