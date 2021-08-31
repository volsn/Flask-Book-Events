"""
Module for Event Endpoints
"""
from typing import Dict, Tuple

from flask import request
from flask_babel import gettext as _
from flask_restful import Resource

from models.event import EventModel
from schemas.event import EventSchema
from utils.auth import jwt_required
from utils.pagination import create_pagination

event_schema = EventSchema()
event_list_schema = EventSchema(many=True,
                                exclude=('participants',))


class RetrieveUpdateDestroyEvent(Resource):
    @classmethod
    def get(cls, id_: int) -> Tuple[Dict, int]:
        """
        Retrieve Details on Event
        :param id_: int
        :return: Tuple[Dict, int]
        """
        event = EventModel.find_by_id(id_)
        if event:
            return event_schema.dump(event), 200

        return {'message': _('event_not_found').format(id_)}, 404

    @classmethod
    @jwt_required(admin=True)
    def put(cls, id_: int) -> Tuple[Dict, int]:
        """
        Update Details about Event
        :param id_: int
        :return: Tuple[Dict, int]
        """
        event_json = request.get_json()
        event = EventModel.find_by_id(id_)

        if event:
            event.update_in_db(data=event_json)
            return event_schema.dump(event), 200
        return {'message': _('event_not_found').format(id_)}, 404

    @classmethod
    @jwt_required(admin=True)
    def delete(cls, id_: int) -> Tuple[Dict, int]:
        """
        Delete Event
        :param id_: int
        :return: Tuple[Dict, int]
        """
        event = EventModel.find_by_id(id_)

        if event:
            event.delete_from_db()
            return {'message': _('event_not_found').format(id_)}, 404
        return {'message': _('event_deleted').format(id_)}, 404


class ListCreateEvent(Resource):
    @classmethod
    def get(cls) -> Tuple[Dict, int]:
        """
        Get list of Events. Filter, Ordered and Paginated
        :return: Tuple[Dict, int]
        """
        filters = dict(request.args)
        page = int(filters.pop('page', 1))
        limit = int(filters.pop('limit', 20))

        paginated_events = EventModel.get_list(query_params=filters,
                                               page=page,
                                               limit=limit)

        response = create_pagination(items=paginated_events,
                                     schema=event_list_schema,
                                     page=page,
                                     limit=limit,
                                     query_params=filters,
                                     url=request.base_url)

        return response, 200

    @classmethod
    @jwt_required(admin=True)
    def post(cls) -> Tuple[Dict, int]:
        """
        Create new Event
        :return: Tuple[Dict, int]
        """
        event_json = request.get_json()

        if EventModel.find_by_name(event_json.get('name')):
            return {
                       'message': _('event_already_exists')
                           .format(event_json['name'])
                   }, 400

        event = event_schema.load(event_json)
        event.save_to_db()

        return event_schema.dump(event), 201
