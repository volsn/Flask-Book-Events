from typing import Union

from db import db


class ParticipantModel(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def find_by_id(cls, id_: int) -> Union['ParticipantModel', None]:
        return cls.query.filter_by(id=id_).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
