from datetime import datetime

from flask_babel import format_datetime
from marshmallow import fields, post_load

from ma import ma
from models.event import EventModel
from schemas.participant import ParticipantSchema


class EventSchema(ma.SQLAlchemyAutoSchema):
    start = fields.Method(serialize='dump_start',
                          deserialize='load_datetime')
    end = fields.Method(serialize='dump_end',
                        deserialize='load_datetime')
    participants = fields.Nested(ParticipantSchema, many=True)
    status = fields.String()

    class Meta:
        model = EventModel
        dump_only = ('id',)
        include_fk = True

    @staticmethod
    def dump_start(obj: EventModel) -> str:
        return format_datetime(obj.start)

    @staticmethod
    def dump_end(obj: EventModel) -> str:
        return format_datetime(obj.end)

    @staticmethod
    def load_datetime(value: str) -> datetime:
        return datetime.strptime(value, '%Y.%m.%d %H:%M')

    @post_load
    def make_event(self, data, **kwargs):
        return EventModel(**data)
