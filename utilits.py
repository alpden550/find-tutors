import json
from pathlib import Path
import click

import data as tutors
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


def write_tutors_to_json(output_file='tutors.json'):
    Path(output_file).write_text(
        json.dumps(
            {'goals': tutors.goals, 'teachers': tutors.teachers},
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        ),
    )


def create_goals(goals):
    for name in goals:
        goal = models.Goal(name=name)
        db.session.add(goal)
        click.echo('Added goal {goal}'.format(goal=goal))
    db.session.commit()


def fill_db(input_json=TUTORS_JSON):
    goals = fetch_data_from_json('goals')
    create_goals(goals)


if __name__ == '__main__':
    fill_db()
