import os

import requests
from flask import request
from flask_restful import Resource
from flask_babel import gettext as _

from models.event import EventModel
from models.participant import ParticipantModel
from utils.auth import jwt_required


class EventParticipants(Resource):
    @classmethod
    @jwt_required(admin=True)
    def post(cls, event_id: int):
        event = EventModel.find_by_id(event_id)
        if event is None:
            return {'message': _('event_not_found').format(event_id)}, 404

        body = request.get_json()
        for id_ in body.get('participants'):
            participant = ParticipantModel.find_by_id(id_)

            if participant is None:
                books_url = os.getenv('BOOKS_URL')
                author_details = requests.get(f'{books_url}/api/author/{id_}')
                participant = ParticipantModel(id=id_,
                                               name=author_details.json()
                                               .get('name'))
                participant.save_to_db()

            if participant in event.participants:
                return {
                           'message': _('author_already_registered_for_event')
                       }, 400

            event.participants.append(participant)
            event.save_to_db()

        return {'message': _('registered_for_event')}, 200

    @classmethod
    @jwt_required(admin=True)
    def delete(cls, event_id: int):
        event = EventModel.find_by_id(event_id)
        if event is None:
            return {'message': _('event_not_found')}, 404

        body = request.get_json()
        for id_ in body.get('participants'):
            participant = ParticipantModel.find_by_id(id_)

            if participant is None or participant not in event.participants:
                return {'message': _('author_not_found').format(id_)}, 404

            event.participants.remove(participant)
            event.save_to_db()

        return {'message': _('unregistered_from_event')}, 200


class ParticipantResource(Resource):
    @classmethod
    def get(cls):
        pass

    @classmethod
    @jwt_required(admin=True)
    def put(cls, id_):
        participant = ParticipantModel.find_by_id(id_)
        if participant is None:
            participant = ParticipantModel(id=id_)

        books_url = os.getenv('BOOKS_URL')
        author_details = requests.get(f'{books_url}/api/author/{id_}')

        if author_details.status_code != 200:
            return {'message': _('error_loading_author')}, 500

        participant.name = author_details.json()['name']
        participant.save_to_db()
        return {'message': _('updated_author')}, 200

    @classmethod
    @jwt_required(admin=True)
    def delete(cls, id_):
        participant = ParticipantModel.find_by_id(id_)
        if participant is None:
            return {'message': _('author_not_found').format(id_)}, 404

        participant.delete_from_db()
        return {'message': _('author_deleted')}, 200
