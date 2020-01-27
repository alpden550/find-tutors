import json
from pathlib import Path

import data as tutors


def write_data_to_json(output_file='tutors.json'):
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
    write_data_to_json()
