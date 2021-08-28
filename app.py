import os

import jwt
from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from marshmallow import ValidationError
from dotenv import load_dotenv

from db import db
from ma import ma
from resources.event import RetrieveUpdateDestroyEvent, ListCreateEvent
from resources.guest import Login, CreateRetrieveDestroyGuests
from resources.participant import CreateDestroyParticipants


app = Flask('foo')
load_dotenv('.env')
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URI", "sqlite:///data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = os.getenv('SECRET_KEY')


api = Api(app)
migrate = Migrate(app, db)


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
api.add_resource(CreateRetrieveDestroyGuests,
                 '/events/<int:event_id>/guests')
api.add_resource(CreateDestroyParticipants,
                 '/events/<int:event_id>/participants')
api.add_resource(Login,
                 '/login')

db.init_app(app)
ma.init_app(app)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
