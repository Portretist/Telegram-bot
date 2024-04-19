class IntermediateStorage:
    '''
    Класс Временное хранилище.
    Предоствляет временное хранилище важным данным.
    '''
    number = None

    @classmethod
    def add_store(cls, number: str) -> None:
        '''
        Функция добавить. Записывает переданное значение в хранилище.
        :param number: str
        '''
        cls.number = number

    @classmethod
    def pop_store(cls) -> None:
        '''
        Функция удалить. Заменяет записанное ранее в хранилище на None.
        '''
        cls.number = None
