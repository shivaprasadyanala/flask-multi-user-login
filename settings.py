from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
db = SQLAlchemy(app)


def get_app():
    db.init_app(app)
    migrate = Migrate(app, db)
    from login_app import models
    from login_app import routes
    return app
