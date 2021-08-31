import os
import pickle
import random

from faker import Faker
from  sqlalchemy.sql.expression import func

from app import app
from models.guest import GuestModel
from models.participant import ParticipantModel


app.app_context().push()

from models.event import EventModel

fake = Faker()
client = app.test_client()


def generate_events(num=1000):
    for _ in range(num):
        end_datetime = fake.date_time_between('-1M', '+1M')
        event = EventModel(
            name=fake.sentence(),
            start=fake.date_time_between('-1M', end_datetime),
            end=end_datetime,
            description=fake.text(512)
        )

        for participant in ParticipantModel.query.order_by(func.random()) \
                .limit(random.randint(1, 3)):
            event.participants.append(participant)

        for guest in GuestModel.query.order_by(func.random()) \
                .limit(random.randint(1, 20)):
            event.guests.append(guest)

        event.save_to_db()


def load_participants(path=os.path.join('data', 'authors.pickle')):
    with open(path, 'rb') as file:
        participants = pickle.load(file)

    for name in participants:
        participant = ParticipantModel(name=name)
        participant.save_to_db()


def generate_guests(num=100):
    for _ in range(num):
        guest = GuestModel(name=fake.name())
        guest.save_to_db()


if __name__ == '__main__':
    load_participants()
    generate_guests()
    generate_events()
