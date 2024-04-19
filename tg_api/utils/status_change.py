class ChangeStatus:
    '''
    Класс Изменение статуса.
    Служит как хранилище состояния бота.
    '''
    status = None

    @classmethod
    def add_status(cls, message: str) -> None:
        '''
        Метод добавить статус.
        Записывает в переменную статус, переданную команду(сообщение)
        отражающую состояние бота(поиск одного из трёх типов
         информации(персонаж, локация, эпизод))
        '''
        cls.status = message

    @classmethod
    def pop_status(cls) -> None:
        '''
        Метод удалить статус.
        Меняет содержимое переменной статус на None.
        '''
        cls.status = None


if __name__ == '__main__':
    ChangeStatus()
