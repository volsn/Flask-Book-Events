import os

import requests
from flask import request
from flask_restful import Resource

from models.event import EventModel
from models.participant import ParticipantModel
from utils.auth import jwt_required


class EventParticipants(Resource):
    @classmethod
    @jwt_required(admin=True)
    def post(cls, event_id: int):
        event = EventModel.find_by_id(event_id)
        if event is None:
            return {'message': 'Event not found.'}, 404

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
                return {'message': f'Author with id {id_} '
                                   f'already registered.'}, 400

            event.participants.append(participant)
            event.save_to_db()

        return {'message': 'Successfully registered for Event.'}, 200

    @classmethod
    @jwt_required(admin=True)
    def delete(cls, event_id: int):
        event = EventModel.find_by_id(event_id)
        if event is None:
            return {'message': 'Event not found.'}, 404

        body = request.get_json()
        for id_ in body.get('participants'):
            participant = ParticipantModel.find_by_id(id_)

            if participant is None or participant not in event.participants:
                return {'message': f'Participant with id {id_} not found'}, 404

            event.participants.remove(participant)
            event.save_to_db()

        return {'message': 'Successfully unregister from Event.'}, 200


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
            return {'message': f'Error loading Author details.'}, 500

        participant.name = author_details.json()['name']
        participant.save_to_db()
        return {'message': 'Updated Author.'}, 200

    @classmethod
    @jwt_required(admin=True)
    def delete(cls, id_):
        participant = ParticipantModel.find_by_id(id_)
        if participant is None:
            return {'message': f'Author with id {id_} not found.'}, 404

        participant.delete_from_db()
        return {'message': 'Author successfully deleted.'}, 200
