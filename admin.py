from flask_admin.contrib.sqla import ModelView

from utils.mixins import AdminRequiredMixin


class EventAdmin(AdminRequiredMixin, ModelView):
    # column_hide_backrefs = False  # TODO
    can_export = True
    column_searchable_list = ('name', 'description',)
    column_list = ('id', 'name', 'start', 'end', 'description', 'guests')


class ParticipantAdmin(AdminRequiredMixin, ModelView):
    can_export = True
    column_searchable_list = ('name',)
    column_list = ('id', 'name',)


class GuestAdmin(AdminRequiredMixin, ModelView):
    can_export = True
    column_searchable_list = ('name',)
    column_list = ('id', 'name',)
