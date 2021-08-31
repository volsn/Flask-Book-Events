"""
Module with Event Related Models
"""
from datetime import datetime
from typing import Dict, Optional

from flask_sqlalchemy import Pagination, BaseQuery
from sqlalchemy import and_

from db import db
from models.guest import GuestModel
from models.participant import ParticipantModel


class GuestEventModel(db.Model):
    """
    Model used to create Many-to-Many relationship between event and guests
    """
    __tablename__ = 'guest_event'
    guest_id = db.Column(db.Integer(),
                         db.ForeignKey('guests.id', ondelete='CASCADE'),
                         primary_key=True)
    event_id = db.Column(db.Integer(),
                         db.ForeignKey('events.id', ondelete='CASCADE'),
                         primary_key=True)


class ParticipantEventModel(db.Model):
    """
    Model used to create Many-to-Many
    relationship between event and participants
    """
    __tablename__ = 'participant_event'
    participant_id = db.Column(db.Integer(),
                               db.ForeignKey('participants.id',
                                             ondelete='CASCADE'),
                               primary_key=True)
    event_id = db.Column(db.Integer(),
                         db.ForeignKey('events.id', ondelete='CASCADE'),
                         primary_key=True)


class EventModel(db.Model):
    """
    Event Model
    """
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    description = db.Column(db.String(512), nullable=True)
    participants = db.relationship(ParticipantModel,
                                   secondary='participant_event',
                                   backref=db.backref('events',
                                                      lazy='dynamic'),
                                   cascade='all, delete')
    guests = db.relationship(GuestModel,
                             secondary='guest_event',
                             backref=db.backref('events', lazy='dynamic'),
                             cascade='all, delete')

    def __str__(self) -> str:
        """
        String representation of the Object
        :return: str
        """
        return self.name

    @property
    def status(self) -> str:
        """
        Property for Event Status
        :return: str
        """
        if self.end < datetime.now():
            return 'past'
        elif self.start > datetime.now():
            return 'upcoming'
        return 'ongoing'

    @classmethod
    def find_by_name(cls, name: str) -> Optional['EventModel']:
        """
        Method for finding event by its name.
        Returns None when object is not found
        :param name: str
        :return: Optional['EventModel']
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_: int) -> Optional['EventModel']:
        """
        Method for finding event by its id.
        Returns None when object is not found
        :param id_: int
        :return: Optional['EventModel']
        """
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def filter_by_status(cls, status: str,
                         queryset: Optional[BaseQuery] = None) -> BaseQuery:
        """
        Filter given query by status using the start and end time of events
        :param status: str
        :param queryset: Optional[BaseQuery] = None
        :return: BaseQuery
        """
        queryset = queryset or cls.query
        current_timestamp = datetime.now()
        filters = {
            'past': cls.end < current_timestamp,
            'upcoming': cls.start > current_timestamp,
            'ongoing': and_(cls.start < current_timestamp,
                            cls.end > current_timestamp),
        }
        return queryset.filter(filters.get(status))

    @classmethod
    def filter_by_participant(cls, id_: int,
                              queryset: Optional[BaseQuery] = None) \
            -> BaseQuery:
        """
        Filter given query by participant
        :param id_: int
        :param queryset: Optional[BaseQuery] = None
        :return: BaseQuery
        """
        id_ = int(id_)
        queryset = queryset or cls.query
        return queryset.join(ParticipantEventModel) \
            .filter(ParticipantEventModel.participant_id == id_)

    @classmethod
    def filter_by_guest(cls, id_: int,
                        queryset: Optional[BaseQuery] = None) -> BaseQuery:
        """
        Filter given query by guest
        :param id_: int
        :param queryset: Optional[BaseQuery] = None
        :return: BaseQuery
        """
        id_ = int(id_)
        queryset = queryset or cls.query
        return queryset.join(GuestEventModel) \
            .filter(GuestEventModel.guest_id == id_)

    @classmethod
    def get_list(cls, page: int = 1, limit: int = 20,
                 filters: Optional[Dict] = None) -> Pagination:
        """
        Apply specified filters on the object
        and, then order and paginate them
        :param page: int = 1
        :param limit: int = 20
        :param filters: Optional[Dict] = None
        :return: Pagination
        """
        filters = filters or {}
        filter_queries = {
            'status': cls.filter_by_status,
            'participant': cls.filter_by_participant,
            'guest': cls.filter_by_guest,
        }

        query = cls.query
        # Return empty query when user specifies unsupported filter
        plug = lambda x, y: cls.query.filter(False)
        for field, value in filters.items():
            query = filter_queries.get(field, plug)(value, query)
        return query.order_by(cls.id).paginate(page, limit, error_out=False)

    @classmethod
    def get_guests_list(cls, event_id: int, page: int = 1, limit: int = 20) \
            -> Pagination:
        """
        Return ordered and paginated query of a certain event guests
        :param event_id: int
        :param page: int = 1
        :param limit: int = 20
        :return: Pagination
        """
        return GuestModel.query.filter(cls.id == event_id) \
            .order_by(GuestModel.id).paginate(page, limit, error_out=False)

    def save_to_db(self) -> None:
        """
        Save object to the database
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def update_in_db(self, data: Dict) -> None:
        """
        Update data in the database
        :param data: Dict
        :return: None
        """
        EventModel.query.filter_by(id=self.id).update(data)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete object from the database
        :return: None
        """
        db.session.delete(self)
        db.session.commit()
