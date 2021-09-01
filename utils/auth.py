"""
Module with Authentication Utilities
"""
import json
import os
from datetime import datetime
from functools import wraps
from typing import Dict, Callable, Union

import jwt
from flask import request, Response
from flask_babel import gettext as _


class jwt_required:
    """
    Class based decorator for restricting users
    access to endpoints based on JWT token.
    """
    def __init__(self, *, admin: bool = False, owner: bool = False) -> None:
        """
        Initialize Decorator
        :param admin: bool = False
        :param owner: bool = False
        """
        self.admin = admin
        self.owner = owner

    def __call__(self, func: Callable) -> Union[Response, Callable]:
        """
        Check whether user trying to access endpoints have permissions to do so
        :param func: Callable
        :return: Union[Response, Callable]
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token:

                # Check if user is owner of the object he is trying to access
                if self.owner:
                    claims = decode_token(token)
                    if claims.get('id') != kwargs.get('id_'):
                        return Response(json.dumps(
                            {
                                'message': _('owner_or_admin_required')
                            }),
                            status=400,
                            content_type='application/json')

                # Check if user is admin
                if self.admin:
                    claims = decode_token(token)
                    if not claims.get('is_admin'):
                        return Response(json.dumps(
                            {
                                'message': _('admin_required')
                            }),
                            status=400,
                            content_type='application/json')

                return func(*args, **kwargs)

            return Response(json.dumps(
                {
                    'message': _('login_required')
                }),
                status=400,
                content_type='application/json')

        return wrapper


def decode_token(token: str) -> Dict:
    """
    Decode JWT Token with App Secret Key
    :param token: str
    :return: Dict
    """
    claims = jwt.decode(token,
                        os.getenv('SECRET_KEY'),
                        algorithms='HS256')

    if int(claims.get('exp')) < int(datetime.now().strftime('%s')):
        raise jwt.PyJWTError(_('token_expired'))
    return claims
