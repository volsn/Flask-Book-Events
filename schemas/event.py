from marshmallow import fields, post_load

from ma import ma
from models.event import EventModel
from schemas.participant import ParticipantSchema


class EventSchema(ma.SQLAlchemyAutoSchema):
    start = fields.DateTime(format='%Y.%m.%d %H:%M')
    end = fields.DateTime(format='%Y.%m.%d %H:%M')
    # guests = fields.Nested(GuestSchema, many=True)
    participants = fields.Nested(ParticipantSchema, many=True)
    status = fields.String()

    class Meta:
        model = EventModel
        dump_only = ('id',)
        include_fk = True

    @post_load
    def make_event(self, data, **kwargs):
        return EventModel(**data)
