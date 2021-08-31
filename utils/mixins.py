from typing import Dict, Tuple

from flask_babel import gettext as _

from utils.auth import jwt_required


class AdminRequiredMixin:
    @jwt_required(admin=True)
    def is_accessible(self) -> bool:
        return True

    def inaccessible_callback(self, name: str, **kwargs) -> Tuple[Dict, int]:
        return {'message': _('admin_required')}, 400
