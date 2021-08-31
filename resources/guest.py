import json
import os

import requests
from flask import request
from flask_babel import gettext as _
from flask_restful import Resource

from models.event import EventModel
from models.guest import GuestModel
from schemas.guest import GuestSchema
from utils.auth import jwt_required, decode_token
from utils.pagination import create_pagination

guest_list_schema = GuestSchema(many=True)


class Login(Resource):
    @classmethod
    def post(cls):
        books_url = os.getenv('BOOKS_URL')

        response = requests.post(books_url + '/api/login/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(request.get_json()))

        return json.loads(response.text), response.status_code


class EventGuests(Resource):

    @classmethod
    def get(cls, event_id: int):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))

        paginated_events = EventModel.get_guests_list(event_id=event_id,
                                                      page=page,
                                                      limit=limit)

        response = create_pagination(items=paginated_events,
                                     schema=guest_list_schema,
                                     page=page,
                                     url=request.url_root)

        return response, 200

    @classmethod
    @jwt_required()
    def post(cls, event_id: int):
        event = EventModel.find_by_id(event_id)
        if event is None:
            return {'message': _('event_not_found').format(event_id)}, 404

        claims = decode_token(request.headers['Authorization'])

        guest = GuestModel.find_by_id(claims['id'])
        if guest is None:
            books_url = os.getenv('BOOKS_URL')
            user_details = requests.get(f'{books_url}/api/user/{claims["id"]}')
            guest = GuestModel(id=claims['id'],
                               name=user_details.json()['name'])
            guest.save_to_db()

        if guest in event.guests:
            return {'message': _('user_already_registered_for_event')}, 400

        event.guests.append(guest)
        event.save_to_db()

        return {'message': _('registered_for_event')}, 200

    @classmethod
    @jwt_required()
    def delete(cls, event_id: int):
        event = EventModel.find_by_id(event_id)
        if event is None:
            return {'message': _('event_not_found').format(event_id)}, 404

        claims = decode_token(request.headers['Authorization'])

        guest = GuestModel.find_by_id(claims['id'])
        if guest is None or guest not in event.guests:
            return {'message': _('user_not_registered_for_event')}, 400

        event.guests.remove(guest)
        event.save_to_db()

        return {'message': _('unregistered_from_event')}, 200


class GuestResource(Resource):
    @classmethod
    def get(cls):
        pass

    @classmethod
    @jwt_required(admin=True, owner=True)
    def put(cls, id_):
        guest = GuestModel.find_by_id(id_)
        if guest is None:
            guest = GuestModel(id=id_)

        books_url = os.getenv('BOOKS_URL')
        user_details = requests.get(f'{books_url}/api/user/{id_}')

        if user_details.status_code != 200:
            return {'message': _('error_loading_user')}, 500

        guest.name = user_details.json()['name']
        guest.save_to_db()

        return {'message': _('profile_updated')}, 200

    @classmethod
    @jwt_required(admin=True, owner=True)
    def delete(cls, id_):
        guest = GuestModel.find_by_id(id_)
        if guest is None:
            return {'message': _('user_not_found').format(id_)}, 404

        guest.delete_from_db()
        return {'message': _('user_deleted')}, 200
