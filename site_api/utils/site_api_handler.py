url = 'https://rickandmortyapi.com/api'


def create_req_url(info_type: str, id: int) -> str:
    req_url = f'{url}/{info_type}/{id}'
    return req_url


if __name__ == '__main__':
    print(create_req_url('character', 43))
