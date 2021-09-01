"""
Module with Participant Schema
"""
from typing import Dict

from marshmallow import post_load

from ma import ma
from models.participant import ParticipantModel


class ParticipantSchema(ma.SQLAlchemyAutoSchema):
    """
    Participant Schema
    """
    class Meta:
        """
        Connecting schema to Participant Model
        """
        model = ParticipantModel
        dump_only = ('id',)

    @post_load
    def make_participant(self, data: Dict, **kwargs: Dict) -> ParticipantModel:
        """
        Special method for returning ParticipantModel
        object after deserializing
        :param data: Dict
        :param kwargs: Dict
        :return: ParticipantModel
        """
        return ParticipantModel(**data)
