from typing import Dict


def create_pagination(*, items, schema,  page: int = 1,
                      limit: int = 20, query_params: Dict = None, url: str):
    response = {
        'page': page,
        'limit': limit,
    }

    query_params = (query_params or {}).copy()
    query_params = ''.join(
        [f'&{key}={value}' for key, value in query_params.items()])

    next_ = items.next_num
    response[
        'next'] = f'{url}?page={next_}' \
                  f'&limit={limit}{query_params}' if next_ else ''

    prev = items.prev_num
    response[
        'prev'] = f'{url}?page={prev}' \
                  f'&limit={limit}{query_params}' if prev else ''

    response['results'] = schema.dump(items.items)

    return response
