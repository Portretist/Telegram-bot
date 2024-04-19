import functools
import urllib
from typing import Dict, List, Callable

import telebot

from database.common.models import db, Person, History
from database.core import crud
from site_api.utils.intermediate_storage import IntermediateStorage
from site_api.utils.request_info import get_info
from site_api.utils.site_api_handler import create_req_url
from tg_api.config.bot import bot

from tg_api.utils.status_change import ChangeStatus


def logging_response(func) -> Callable:
    db_write = crud.create()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        data = [
            {
                'info_type': args[1],
                'object_id': response['id'],
                'object_name': response['name'],
                'user_id': Person.user_id
            }
        ]

        db_write(db, History, data)
        return response
    return wrapper


class SiteApiInterface:
    '''
    Класс Сайт АПИ Интрефейс.
    Выполняет роль обёртки для методов.
    '''

    @staticmethod
    def check_status(message: telebot.types.Message, status: str, number: str) -> None:
        '''
        Метод Проверка статуса.
        В зависимости от переданного статуса, вызывает
        скрытые методы класса.
        :param message: telebot.types.Message
        :param status: str
        :param number: str
        '''
        print('Вызов метода: проверка статуса')
        try:
            if status == 'find_char':
                print('Успешная проверка статуса - статус find_char')
                SiteApiInterface._char(int(number), message)

            elif status == 'find_loc':
                print('Успешная проверка статуса - статус find_loc')
                SiteApiInterface._loc(int(number), message)

            elif status == 'find_eps':
                print('Успешная проверка статуса - статус find_eps')
                SiteApiInterface._eps(int(number), message)

        except Exception as exc:
            error_message = '{error}\nВоспользуйтесь функцией /help'.format(
                error=exc
            )
            bot.reply_to(message, error_message)

        finally:
            IntermediateStorage.pop_store()
            ChangeStatus.pop_status()

    @staticmethod
    def _char(id_num: int, message: telebot.types.Message) -> None:
        '''
        Скрытый метод Чар(сокращение от character).
        Запрашивает данные с сайта в соответсвии со своим
        типом информации и переданным id.

        Если ответ получен, то:
            Отправляет фотографию из данных.
            Собирает сообщение в соответсвии со своими данными
            и отправлет его.

        Иначе:
            Выводит сообщение об ошибке на стороне сервера(сайта).
        :param id_num: int
        :param message: telebot.types.Message
        '''
        print('Вызов скрытого метода  _char')
        data = SiteApiInterface._main_req(message, 'character', id_num)

        print('Запрос информации о эпизодах')
        eps_names = SiteApiInterface._more_info(message, data, 'episode')

        print('Отправка фотографии')
        with open('out.jpeg', 'wb') as f:
            f.write(urllib.request.urlopen(data['image']).read())
        with open('out.jpeg', 'rb') as img:
            bot.send_photo(message.chat.id, img)

        info_message = 'Номер-id: {id}\nИмя: {name}\nСтатус цели: {status}\nРаса: {species}\nОсобенности: {type}\nПол: {gender}\nПроисхождение: {origin}\nМестонахождение: {location}\nБыл(а) замечен в следующих эпизодах мультсериала: {episode}'.format(
            id=data['id'],
            name=data['name'],
            status=data['status'],
            species=data['species'],
            type=data['type'],
            gender=data['gender'],
            origin=data['origin']['name'],
            location=data['location']['name'],
            episode=eps_names
        )
        bot.send_message(message.chat.id, info_message)

    @staticmethod
    def _loc(id_num: int, message: telebot.types.Message) -> None:
        '''
        Скрытый метод Лок(сокращение от location).
        Запрашивает данные с сайта в соответсвии со своим
        типом информации и переданным id.

        Если ответ получен, то:
            Собирает сообщение в соответсвии со своими данными
            и отправлет его.

        Иначе:
            Выводит сообщение об ошибке на стороне сервера(сайта).
        :param id_num: int
        :param message: telebot.types.Message
        '''
        print('Вызов скрытого метода  _loc')

        data = SiteApiInterface._main_req(message, 'location', id_num)

        print('Запрос информации о персонажах')

        res_names = SiteApiInterface._more_info(message, data, 'residents')
        info_message = 'Номер-id: {id}\nНазвание локации: {name}\nТип: {type}\nИзмерение: {dimension}\nОбитатели: {residents}'.format(
            id=data['id'],
            name=data['name'],
            type=data['type'],
            dimension=data['dimension'],
            residents=res_names
        )
        bot.send_message(message.chat.id, info_message)

    @staticmethod
    def _eps(id_num: int, message: telebot.types.Message) -> None:
        '''
        Скрытый метод Эпс(сокращение от episode).
        Запрашивает данные с сайта в соответсвии со своим
        типом информации и переданным id.

        Если ответ получен, то:
            Собирает сообщение в соответсвии со своими данными
            и отправлет его.

        Иначе:
            Выводит сообщение об ошибке на стороне сервера(сайта).
        :param id_num: int
        :param message: telebot.types.Message
        '''
        print('Вызов скрытого метода  _eps')

        data = SiteApiInterface._main_req(message, 'episode', id_num)
        print(data)

        print('Запрос информации о персонажах')

        char_names = SiteApiInterface._more_info(message, data, 'characters')
        info_message = 'Номер-id: {id}\nНазвание эпизода: {name}\nНомер сезона и серии: {episode}\nДата выхода: {air_date}\nУчастники эпизода: {characters}'.format(
            id=data['id'],
            name=data['name'],
            episode=data['episode'],
            air_date=data['air_date'],
            characters=char_names
        )
        bot.send_message(message.chat.id, info_message)

    @staticmethod
    @logging_response
    def _main_req(message: telebot.types.Message, info_type: str, id_num: int) -> Dict:
        '''
        Скрытый метод Основной запрос.
        Выполняет функцию модели для запроса информации с сайта.
        Возвращает результат работы функций get_info и create_req_url в виде словаря.

        :param id_num: int
        :param info_type: str
        :param message: telebot.types.Message

        :return dict
        :rtype Dict
        '''
        bot.send_message(message.chat.id, 'Отправлен запрос на галактический сервер. Ждите..')
        print('Запрос основной информации')
        return get_info(create_req_url(info_type, id_num))

    @staticmethod
    def _more_info(message: telebot.types.Message, data: Dict, info_type: str) -> List:
        '''
        Скрытый метод Больше информации.
        Выполняет функцию модели для запроса информации с сайта.
        Очищает временное хранилище и и изменяет статус бота.
        Возвращает результат работы функций get_info для элементов по ключу info_type в словаре data в виде списка.

        :param data: Dict
        :param info_type: str
        :param message: telebot.types.Message

        :return result
        :rtype list
        '''
        bot.send_message(message.chat.id, 'Запрос дополнительной информации..')
        print('Запрос дополнителной информации')
        work_lst = [get_info(i_elem) for i_elem in data[info_type]]

        if info_type == 'characters':
            name = 'Имя участника:'

        elif info_type == 'episode':
            name = 'Название эпизода:'

        elif info_type == 'residents':
            name = 'Имя обитателя:'

        result = [(name, i_elem['name'], 'Номер-id:', i_elem['id']) for i_elem in work_lst]
        bot.send_message(message.chat.id, 'Ответ получен!')
        print('Запрос удовлетворён')
        return result


if __name__ == '__main__':
    SiteApiInterface()
    logging_response()
