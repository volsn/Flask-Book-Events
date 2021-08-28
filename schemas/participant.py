from marshmallow import post_load

from ma import ma
from models.participant import ParticipantModel


class ParticipantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ParticipantModel
        dump_only = ('id',)

    @post_load
    def make_participant(self, data, **kwargs):
        return ParticipantModel(**data)
