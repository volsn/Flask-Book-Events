"""
Pagination Utilities
"""
from typing import Dict, Optional

from flask_sqlalchemy import Pagination
from marshmallow import Schema


def create_pagination(*, items: Pagination, schema: Schema,  page: int = 1,
                      limit: int = 20, query_params: Optional[Dict] = None,
                      url: str) -> Dict:
    """
    Create response from paginated items by adding a number of params,
    such as links next and previous pages and other
    :param items: Sequence
    :param schema: Schema
    :param page: int = 1
    :param limit: int = 20
    :param query_params: Optional[Dict]
    :param url: str
    :return: Dict
    """
    response = {
        'page': page,
        'limit': limit,
    }

    # Create url path out of given parameters
    query_params = (query_params or {}).copy()
    query_params = ''.join(
        [f'&{key}={value}' for key, value in query_params.items()])

    # Add next page link or None
    next_ = items.next_num
    response[
        'next'] = f'{url}?page={next_}' \
                  f'&limit={limit}{query_params}' if next_ else None

    # Add next previous link or None
    prev = items.prev_num
    response[
        'prev'] = f'{url}?page={prev}' \
                  f'&limit={limit}{query_params}' if prev else None

    response['results'] = schema.dump(items.items)

    return response
