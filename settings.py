import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


class BaseConfig(object):
    DEBUG = os.getenv('DEBUG') in {'1', 'yes', 'true', 'True'} or False
    SECRET_KEY = os.getenv('SECRET_KEY', 'some extra secret string')

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///{db}'.format(db=os.path.join(basedir, 'data.sqlite')),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
