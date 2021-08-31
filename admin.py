from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from models.event import EventModel, guest_event, participant_event
from models.participant import ParticipantModel
from models.guest import GuestModel

from utils.mixins import AdminRequiredMixin


class EventModelAdmin(AdminRequiredMixin):
    can_export = True
    column_searchable_list = ('name', 'description',)
    column_list = ('id', 'name', 'start', 'end', 'description',)

