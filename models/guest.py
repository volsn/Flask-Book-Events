from typing import Union
from db import db


class GuestModel(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def find_by_id(cls, id_: int) -> Union['GuestModel', None]:
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def get_list(cls, event_id: int, page: int = 1, limit: int = 20):
        return cls.query.filter_by(event_id=event_id).paginate(page, limit)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
