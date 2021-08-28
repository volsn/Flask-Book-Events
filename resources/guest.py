import json
import os

import requests
from flask import request
from flask_restful import Resource

from models.event import EventModel
from models.guest import GuestModel
from utils.auth import jwt_required, decode_token


class Login(Resource):
    @classmethod
    def post(cls):
        books_url = os.getenv('BOOKS_URL')

        response = requests.post(books_url + '/api/login/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(request.get_json()))

        return json.loads(response.text), response.status_code


class CreateRetrieveDestroyGuests(Resource):

    @classmethod
    def get(cls):
        pass

    @classmethod
    @jwt_required()
    def post(cls, event_id: int):
        event = EventModel.find_by_id(event_id)
        if event is None:
            return {'message': 'Event not found.'}, 404

        claims = decode_token(request.headers['Authorization'])

        guest = GuestModel.find_by_id(claims['id'])
        if guest is None:
            books_url = os.getenv('BOOKS_URL')
            user_details = requests.get(f'{books_url}/api/user/{claims["id"]}')
            guest = GuestModel(id=claims['id'],
                               name=user_details.json()['name'])
            guest.save_to_db()

        if guest in event.guests:
            return {'message': 'Already registered.'}, 400

        event.guests.append(guest)
        event.save_to_db()

        return {'message': 'Successfully registered for Event.'}, 200

    @classmethod
    @jwt_required()
    def delete(cls, event_id: int):
        event = EventModel.find_by_id(event_id)
        if event is None:
            return {'message': 'Event not found.'}, 404

        claims = decode_token(request.headers['Authorization'])

        guest = GuestModel.find_by_id(claims['id'])
        if guest is None or guest not in event.guests:
            return {'message': 'You are not registered for Event.'}, 400

        event.guests.remove(guest)
        event.save_to_db()

        return {'message': 'Successfully unregister from Event.'}, 200
