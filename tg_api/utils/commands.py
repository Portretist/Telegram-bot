from peewee import IntegrityError

from database.common.models import db, Person, History
from database.core import crud
from site_api.core import SiteApiInterface
from tg_api.config.bot import bot
from telebot import types

from site_api.utils.intermediate_storage import IntermediateStorage
from tg_api.utils.status_change import ChangeStatus

comm_lst = '\n/start - Запуск бота\n/help - Вывод функционала бота\n'
search_comm = '\n/find_char - Поиск информации о персонаже\n/find_loc - Поиск информации о локации\n/find_eps - Поиск информации о эпизоде\n'
input_message = 'Введите уникальный номер-id искомого объекта. В соответсвии с межгалактической дерективой Из|Ба, номер-id должен представлять из себя натуральное положительное число(любое число без дробной части и больше нуля)'
date_format = '%d.%m.%Y'


def start_message(message) -> None:
    '''
    Функия Старт-сообщение. Создаёт горячие клавиши, благодаря котором
    можно легко обратиться к функциям бота.
    Так же выводит приветсвтвенное сообщение.
    :param message: telebot.types.Message
    '''
    print('Создание хот-кейев и вывод приветственного сообщения')
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    db_write = crud.create()

    try:
        user_data = [{'user_id': user_id, 'username': username, 'first_name': first_name}]
        db_write(db, Person, user_data)

        welcome_message = "Здравствуйте, гражданин! Я - ваш (не слишком)интеллектуальный ассистент TG-001/SlBx, но вы можете называть меня ТГшка. Добро пожаловать в хранилище данных по объекту 'Rick Sanchez'. Мы собрали всю имеющуюся информацию о путешествиях данного индивида, для быстрого доступа к интересующим вас данным. Сектрет создания тёмной материи будет наш и удачной охоты!"

    except IntegrityError:
        welcome_message = 'С возвращением, гражданин {user}!'.format(
            user=first_name)

    finally:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot_info = types.KeyboardButton("Помощь")
        history_info = types.KeyboardButton("История запросов")

        markup.add(bot_info, history_info)

        bot.send_message(message.chat.id, welcome_message, reply_markup=markup)


def help_message(message) -> None:
    '''
    Функия Помощь-сообщение.
    Выводит спискок обрабатываемых команд.
    :param message: telebot.types.Message
    '''
    print('Вывод списка команд')
    bot.send_message(message.chat.id,
                     """
                     Вот список моих команд:\n{base_comm}\n{optional_comm}
                     """.format(
                         base_comm=comm_lst,
                         optional_comm=search_comm
                     )
                     )


def show_history(message) -> None:
    '''
    Функция Показать Историю.
    Отправляет список всех выполненных(удовлетворённых и отправленных) запросов.
    '''

    user_id = message.from_user.id
    user = Person.get_or_none(Person.user_id == user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    db_read = crud.retrieve()
    retrieved = db_read(
        db,
        History,
        History.request_id,
        History.created_at,
        History.object_name,
        History.object_id,
        History.info_type,
    )

    result = ''
    for elem in retrieved:
        print(Person.history)
        info_message = '\n{request_id}. {info_type} - {object_id}: {object_name}\nДата запроса: {created_at}\n'.format(
            request_id=elem.request_id,
            info_type=elem.info_type,
            object_id=elem.object_id,
            object_name=elem.object_name,
            created_at=elem.created_at.strftime(date_format)
        )
        result = result + info_message

    if result == '':
        bot.send_message(message.chat.id, 'Вы ещё ничего не искали /help')
        return
    else:
        bot.send_message(message.chat.id, result)


def chatterbox(message) -> None:
    '''
    Функия Балаболка.
    Обрабатывает ввводимый пользователем текст.

        -Если введённый текст является горячей клавишей,
        то вызывается соотвевтствующая функция.

        -Если введённый текст является числом, то проводится
        проверка какого типа это число.

        -Если число не является положительным и больше нуля,
        то оно не обрабатывается.

        -Если число не является натуральным,
        то выводиться сообщние подсказка.

        -Если число является положительным, натуральным и больше нуля,
        то оно записывается во временное хранилище:

            -Если статус бота неопределён,
            то выводиться сообщение вопрос с выбором
            одного из статусов.

            -Если статус бота определён,
            то вызывается функция проверки статуса:

                -файл: site_api/core
                -класс: SiteApiInterface
                -метод: check_status

        -Если введённый текст не является ни чем,
        то бот отправит сообщение подсказку.


    :param message: telebot.types.Message
    '''
    if message.chat.type == 'private':

        if message.text == 'Помощь':
            help_message(message)

        elif message.text == 'История запросов':
            show_history(message)

        elif int(message.text.isdigit()) > 0:
            IntermediateStorage.add_store(message.text)

            if ChangeStatus.status is None:
                bot.reply_to(message, 'К какому типу информации относится этот id?' + search_comm)

            else:
                SiteApiInterface.check_status(message, ChangeStatus.status, IntermediateStorage.number)

        else:
            bot.reply_to(message, """
            Извини, я не знаю что ответить. Воспользуйтесь функцией /help
            """)


if __name__ == '__main__':
    start_message()
    help_message()
    chatterbox()
