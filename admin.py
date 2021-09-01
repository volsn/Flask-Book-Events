"""
Module for defining Admin Panel related Stuff
"""
from flask_admin.contrib.sqla import ModelView

from utils.mixins import AdminRequiredMixin


class EventAdmin(AdminRequiredMixin, ModelView):
    """
    Admin Panel Settings for Event Model
    """
    column_hide_backrefs = False
    can_export = True
    column_searchable_list = ('name', 'description',)
    column_list = ('id', 'name', 'start', 'end',
                   'description', 'participants',)


class ParticipantAdmin(AdminRequiredMixin, ModelView):
    """
    Admin Panel Settings for Participant Model
    """
    can_export = True
    column_searchable_list = ('name',)
    column_list = ('id', 'name',)


class GuestAdmin(AdminRequiredMixin, ModelView):
    """
    Admin Panel Settings for Guest Model
    """
    can_export = True
    column_searchable_list = ('name',)
    column_list = ('id', 'name',)
