"""
Module for Guest Model
"""
from typing import Optional

from db import db


class GuestModel(db.Model):
    """
    Guest Model
    """
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False, unique=True)

    def __str__(self) -> str:
        """
        String representation of the Object
        :return: str
        """
        return self.name

    @classmethod
    def find_by_id(cls, id_: int) -> Optional['GuestModel']:
        """
        Method for finding event by its id.
        Returns None when object is not found
        :param id_: int
        :return: Optional['GuestModel']
        """
        return cls.query.filter_by(id=id_).first()

    def save_to_db(self) -> None:
        """
        Save object to the database
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete object from the database
        :return: None
        """
        db.session.delete(self)
        db.session.commit()
