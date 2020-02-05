import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    FLASK_DEBUG = os.getenv('DEBUG') in {'1', 'true'} or False
    SECRET_KEY = os.getenv('SECRET_KEY', 'some extra secret string')

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///{db}'.format(db=os.path.join(basedir, 'data.sqlite')),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG_TB_INTERCEPT_REDIRECTS = False
