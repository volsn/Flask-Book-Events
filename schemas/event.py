"""
Module with Event Schema
"""
from datetime import datetime
from plistlib import Dict

from flask_babel import format_datetime
from marshmallow import fields, post_load

from ma import ma
from models.event import EventModel
from schemas.participant import ParticipantSchema


class EventSchema(ma.SQLAlchemyAutoSchema):
    """
    Event Schema. Sort of 'generic' serializer for Event Model
    """
    start = fields.Method(serialize='dump_start',
                          deserialize='load_datetime')
    end = fields.Method(serialize='dump_end',
                        deserialize='load_datetime')
    participants = fields.Nested(ParticipantSchema, many=True)
    status = fields.String()

    class Meta:
        """
        Connecting schema to Event Model
        """
        model = EventModel
        dump_only = ('id', 'participants',)
        include_fk = True

    @staticmethod
    def dump_start(obj: EventModel) -> str:
        """
        Dump start datetime according to User's local format
        :param obj: EventModel
        :return: str
        """
        return format_datetime(obj.start)

    @staticmethod
    def dump_end(obj: EventModel) -> str:
        """
        Dump end datetime according to User's local format
        :param obj: EventModel
        :return: str
        """
        return format_datetime(obj.end)

    @staticmethod
    def load_datetime(value: str) -> datetime:
        """
        Deserializer input String to Python Datetime
        :param value: str
        :return: datetime
        """
        return datetime.strptime(value, '%Y.%m.%d %H:%M')

    @post_load
    def make_event(self, data: Dict, **kwargs: Dict) -> EventModel:
        """
        Special method for returning EventModel object after deserializing
        :param data: Dict
        :param kwargs: Dict
        :return: EventModel
        """
        return EventModel(**data)
