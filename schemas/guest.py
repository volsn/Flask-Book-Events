from marshmallow import post_load

from ma import ma
from models.guest import GuestModel


class GuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GuestModel

    @post_load
    def make_guest(self, data, **kwargs):
        return GuestModel(**data)
