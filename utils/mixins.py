"""
App Mixins
"""
from typing import Dict, Tuple

from flask import request
from flask_babel import gettext as _


class AdminRequiredMixin:
    """
    Check if user is admin based on the allowed hosts list.
    Used for restricting access to the admin panel
    """
    allowed_hosts = ('127.0.0.1',)

    def is_accessible(self) -> bool:
        """
        Check whether user is admin
        :return: bool
        """
        return request.remote_addr in self.allowed_hosts

    @staticmethod
    def inaccessible_callback(name: str, **kwargs: Dict) -> Tuple[Dict, int]:
        """
        Return error message
        :param name: str
        :param kwargs: Dict
        :return: Tuple[Dict, int]
        """
        return {'message': _('admin_required')}, 400
