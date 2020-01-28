import json
from pathlib import Path

import data as tutors

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


if __name__ == '__main__':
    write_tutors_to_json()
