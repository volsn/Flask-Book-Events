from typing import Dict, Tuple

from flask import request
from flask_babel import gettext as _


class AdminRequiredMixin:
    allowed_hosts = ('127.0.0.1',)

    def is_accessible(self) -> bool:
        return request.remote_addr in self.allowed_hosts

    @staticmethod
    def inaccessible_callback(name: str, **kwargs) -> Tuple[Dict, int]:
        return {'message': _('admin_required')}, 400
