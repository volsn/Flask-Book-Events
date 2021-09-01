"""
Module with Guest Schema
"""
from typing import Dict

from marshmallow import post_load

from ma import ma
from models.guest import GuestModel


class GuestSchema(ma.SQLAlchemyAutoSchema):
    """
    Guest Schema
    """
    class Meta:
        """
        Connecting schema to Guest Model
        """
        model = GuestModel

    @post_load
    def make_guest(self, data: Dict, **kwargs: Dict) -> GuestModel:
        """
        Special method for returning GuestModel object after deserializing
        :param data: Dict
        :param kwargs: Dict
        :return: GuestModel
        """
        return GuestModel(**data)
