import json

from flask import (
    Flask, render_template, request
)
from flask_session import Session
from models import db
import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

with open('config.json', 'r') as f:
    for k, v in json.load(f).items():
        app.config[k] = v

Session(app)
with app.app_context():
    db.init_app(app)
    db.create_all()

app.register_blueprint(api.api_root, url_prefix="/api")
app.register_blueprint(api.api_admin, url_prefix="/api/admin")
app.register_blueprint(api.api_users, url_prefix="/api")

if __name__ == '__main__':
    app.debug = True
    app.run()
