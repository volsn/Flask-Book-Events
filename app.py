import os

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_babel import Babel
from flask_admin import Admin
from marshmallow import ValidationError

from db import db
from ma import ma
from admin import EventModelAdmin
from resources.event import RetrieveUpdateDestroyEvent, ListCreateEvent
from resources.guest import Login, EventGuests, GuestResource
from resources.participant import EventParticipants, ParticipantResource
from models.event import EventModel


app = Flask('foo')
load_dotenv('.env')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI', 'sqlite:///data.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.secret_key = os.getenv('SECRET_KEY')

api = Api(app)
babel = Babel(app)
admin = Admin(app, name='Events', template_mode='bootstrap4')
migrate = Migrate(app, db)


@babel.localeselector
def get_locale():
    return 'en'


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@app.errorhandler(jwt.PyJWTError)
def handle_jwt_error(err):
    return jsonify({'message': str(err)}), 400


api.add_resource(ListCreateEvent,
                 '/events')
api.add_resource(RetrieveUpdateDestroyEvent,
                 '/events/<int:id_>')
api.add_resource(EventGuests,
                 '/events/<int:event_id>/guests')
api.add_resource(EventParticipants,
                 '/events/<int:event_id>/participants')
api.add_resource(Login,
                 '/login')
api.add_resource(GuestResource,
                 '/guests/<int:id_>')
api.add_resource(ParticipantResource,
                 '/participants/<int:id_>')


admin.add_view(EventModelAdmin(EventModel, db.session))

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)

    app.run(port=5000, debug=True)
