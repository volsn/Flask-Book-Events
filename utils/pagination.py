from typing import Dict

from flask_restful import reqparse
from flask_babel import gettext as _


def create_parser() -> reqparse.RequestParser:
    pagination_parser = reqparse.RequestParser()
    pagination_parser.add_argument('page', type=int, default=1,
                                   help=_('page_number'))
    pagination_parser.add_argument('limit', type=int, default=20,
                                   help=_('limit'))
    return pagination_parser


def create_pagination(*, items, schema,  page: int = 1,
                      limit: int = 20, query_params: Dict = None, url: str):
    response = {
        'page': page,
        'limit': limit,
    }

    query_params = query_params or {}
    query_params = ''.join(
        [f'&{key}={value}' for key, value in query_params.items()])

    next_ = items.next_num
    response[
        'next'] = f'{url}?page={next_}' \
                  f'&limit={limit}{query_params}' if next_ else ''

    prev = items.next_num
    response[
        'prev'] = f'{url}?page={prev}' \
                  f'&limit={limit}{query_params}' if prev else ''

    response['results'] = schema.dump(items.items)

    return response
