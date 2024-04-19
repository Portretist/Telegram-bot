import json
from typing import Dict

import requests
from requests import ConnectTimeout


def get_info(req_url, success=200, not_found=404) -> Dict:
    '''
    Функция Получить информацию.
    Создаёт запрос по переданной ссылке.

    В случае если статус код равен параметру успех -
    Обрабатывает результат с помощью json.
    Возвращает словарь.

    В случае если статус код равен параметру не найден -
    вызывает исключение.

    Во всех прочих случаях -
    вызывает исключение.

    :param message: telebot.types.Message
    :param req_url: str
    :param success: int
    :param not_found: int
    :return: response
    :rtype: Dict
    '''
    print('Запрос на сайт')

    try:
        req = requests.get(req_url)
        if req.status_code == success:
            response = json.loads(req.text)
            return response
        elif req.status_code == not_found:
            raise Exception('Объект не найден')

    except ConnectTimeout:
        raise Exception('Ошибка на строне сервера')


if __name__ == '__main__':
    print(get_info('https://rickandmortyapi.com/api/character/2'))

