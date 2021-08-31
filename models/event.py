from datetime import datetime
from typing import Dict, Union, Any, Optional

from flask_sqlalchemy import Pagination, BaseQuery
from sqlalchemy import and_

from db import db
from models.guest import GuestModel
from models.participant import ParticipantModel


class GuestEventModel(db.Model):
    __tablename__ = 'guest_event'
    guest_id = db.Column(db.Integer(),
                         db.ForeignKey('guests.id', ondelete='CASCADE'),
                         primary_key=True)
    event_id = db.Column(db.Integer(),
                         db.ForeignKey('events.id', ondelete='CASCADE'),
                         primary_key=True)


class ParticipantEventModel(db.Model):
    __tablename__ = 'participant_event'
    participant_id = db.Column(db.Integer(),
                               db.ForeignKey('participants.id',
                                             ondelete='CASCADE'),
                               primary_key=True)
    event_id = db.Column(db.Integer(),
                         db.ForeignKey('events.id', ondelete='CASCADE'),
                         primary_key=True)


class EventModel(db.Model):
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

    def __str__(self):
        return self.name

    @property
    def status(self):
        if self.end < datetime.now():
            return 'past'
        elif self.start > datetime.now():
            return 'upcoming'
        return 'ongoing'

    @classmethod
    def find_by_name(cls, name: str) -> 'EventModel':
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_: int) -> 'EventModel':
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def filter_by_status(cls, status: str,
                         queryset: Optional[BaseQuery] = None) -> BaseQuery:
        queryset = queryset or cls.query
        current_timestamp = datetime.now()
        filters = {
            'past': cls.end < current_timestamp,
            'upcoming': cls.start > current_timestamp,
            'ongoing': and_(cls.start < current_timestamp,
                            cls.end > current_timestamp)
        }
        return queryset.filter(filters.get(status))

    @classmethod
    def filter_by_participant(cls, id_: int,
                              queryset: Optional[BaseQuery] = None) \
            -> BaseQuery:
        id_ = int(id_)
        queryset = queryset or cls.query
        return queryset.join(ParticipantEventModel)\
            .filter(ParticipantEventModel.participant_id == id_)

    @classmethod
    def get_list(cls, page: int, limit: int, filters: Dict = None) \
            -> Pagination:
        filters = filters or {}
        filter_queries = {
            'status': cls.filter_by_status,
            'participant': cls.filter_by_participant,
        }

        query = cls.query
        plug = lambda x, y: y
        for field, value in filters.items():
            query = filter_queries.get(field, plug)(value, query)
        return query.order_by(cls.id).paginate(page, limit, error_out=False)

    @classmethod
    def get_guests_list(cls, event_id: int, page: int = 1, limit: int = 20) \
            -> Pagination:
        return GuestModel.query.filter(cls.id == event_id) \
            .order_by(GuestModel.id).paginate(page, limit, error_out=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update_in_db(self, data) -> None:
        EventModel.query.filter_by(id=self.id).update(data)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
