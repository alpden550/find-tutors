# Find-tutors

[![Maintainability](https://api.codeclimate.com/v1/badges/0c71ce568b99270b73b1/maintainability)](https://codeclimate.com/github/alpden550/find-tutors/maintainability) [![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Flask web-application to find tutors to improve your English skills.

## How to install

Download code or clone it from Github, and install dependencies.

If you have already installed Poetry, type command:

```bash
poetry install --no-dev
```

If not, should use a virtual environment for the best project isolation. Activate venv and install dependencies:

```bash
pip install -r requirements.txt
```

Set environment variables:

```bash
export DEBUG=true, if debug mode is need
export SECRET_KEY=some extra secret key
```

## How to run

To fill database run command:

```bash
flask forge
```

It will create goals and tutors from json.

And start web server:

```bash
flask run
```

To create empty db run command:

```bash
flask init
```
