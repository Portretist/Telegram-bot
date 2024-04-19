import telebot.util

from site_api.core import SiteApiInterface
from site_api.utils.intermediate_storage import IntermediateStorage
from tg_api.utils.status_change import ChangeStatus
from .utils.commands import start_message, help_message, chatterbox
from tg_api.config.bot import bot


input_message = 'Введите уникальный номер-id искомого объекта. В соответсвии с межгалактической дерективой Из|Ба, номер-id должен представлять из себя натуральное положительное число(любое число без дробной части и больше нуля)'


class Run:
    '''
    Класс Запустить.
    Служит для запуска бота и как обертка для методов.
    '''
    print('Запуск бота')

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start(message) -> None:
        '''
        Метод Старт.
        В случает вызова команды старт, вызывает
        функцию старт-сообщение.
        :param message: telebot.types.Message
        '''
        print('Вызов функции старт')
        start_message(message)

    @staticmethod
    @bot.message_handler(commands=['help'])
    def help(message) -> None:
        '''
        Метод Помощь.
        В случает вызова команды помощь, вызывает
        функцию помощь-сообщение.
        :param message: telebot.types.Message
        '''
        print('Вызов функции помощь')
        help_message(message)

    @staticmethod
    @bot.message_handler(commands=['find_char', 'find_loc', 'find_eps'])
    def info(message) -> None:
        '''
        Метод Инфо.
        В случает вызова одной из описанных команд,
        эта команда записывается в ChangeStatus как
        статус бота.
        -Если во временном хранилище(IntermediateStorage) нет данных,
        то выйдет сообщение подсказка.
        -Если во временном хранилище(IntermediateStorage) есть данные,
        то выйдет сообщение подсказка,
        а также вызовется метод check_status класса SiteApiInterface
        из site_api/core.

        :param message: telebot.types.Message
        '''
        print('Вызов функции инфо')
        ChangeStatus.add_status(telebot.util.extract_command(message.text))
        if IntermediateStorage.number is None:
            bot.reply_to(message, input_message)
        else:
            bot.reply_to(message, 'Ведётся поиск информации...')
            SiteApiInterface.check_status(message, ChangeStatus.status, IntermediateStorage.number)

    @staticmethod
    @bot.message_handler(content_types=['text'])
    def talker(message) -> None:
        '''
        Метод болтун.
        В случает вызова если введённый текст не является командой,
        то вызывается функция балабол.
        :param message: telebot.types.Message
        '''
        print('Вызов функции болтун')
        chatterbox(message)


bot.infinity_polling()

if __name__ == '__main__':
    Run()


