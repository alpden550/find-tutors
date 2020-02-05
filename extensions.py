from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
csrf = CSRFProtect()
migrate = Migrate()
