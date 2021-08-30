import json
import os
from datetime import datetime
from functools import wraps
from typing import Dict, Callable, Union

import jwt
from flask import request, Response


class jwt_required:
    def __init__(self, *, admin: bool = False, owner: bool = False) -> None:
        self.admin = admin
        self.owner = owner

    def __call__(self, func: Callable) -> Union[Response, Callable]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token:

                if self.owner:
                    claims = decode_token(token)
                    if claims.get('id') != kwargs.get('id_'):
                        return Response(json.dumps(
                            {
                                'message': 'Owner or Admin Rights Required'
                            }),
                            status=400,
                            content_type='application/json')

                if self.admin:
                    claims = decode_token(token)
                    if not claims.get('is_admin'):
                        return Response(json.dumps(
                            {
                                'message': 'Admin Rights required.'
                            }),
                            status=400,
                            content_type='application/json')

                return func(*args, **kwargs)

            return Response(json.dumps(
                {
                    'message': 'Authorization required.'
                }),
                status=400,
                content_type='application/json')

        return wrapper


def decode_token(token: str) -> Dict:
    claims = jwt.decode(token,
                        os.getenv('SECRET_KEY'),
                        algorithms='HS256')

    if int(claims.get('exp')) < int(datetime.now().strftime('%s')):
        raise jwt.PyJWTError('Token expired.')
    return claims
