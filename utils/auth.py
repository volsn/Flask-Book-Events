import os
from datetime import datetime
from functools import wraps
from typing import Dict, Callable, Union

import jwt
from flask import request, Response


class jwt_required:
    def __init__(self, admin: bool = False) -> None:
        self.admin = admin

    def __call__(self, func: Callable) -> Union[Response, Callable]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token:

                if self.admin:
                    claims = decode_token(token)
                    if not claims.get('is_admin'):
                        return Response({'message': 'Admin Rights required.'},
                                        status=400)

                return func(*args, **kwargs)

            return Response({'message': 'Authorization required.'},
                            status=400)

        return wrapper


def decode_token(token: str) -> Dict:
    claims = jwt.decode(token,
                        os.getenv('SECRET_KEY'),
                        algorithms='HS256')

    if int(claims.get('exp')) < int(datetime.now().strftime('%s')):
        raise jwt.PyJWTError('Token expired.')
    return claims
