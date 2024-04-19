from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('rick_und_morty.db')
date_format = '%d.%m.%Y'


class ModelBase(pw.Model):
    '''
    Родительский класс Базовая модель. Наследуется от Модели орм.
    '''
    class Meta():
        database = db


class Person(ModelBase):
    '''
    Класс наследник Персона. Наследуется от Базовой модели.
    Хранит Информацию о пользователе, а именно:
    Его id, никнейм и имя.
    '''
    user_id = pw.IntegerField(primary_key=True)
    username = pw.CharField()
    first_name = pw.CharField()


class History(ModelBase):
    '''
    Класс наследник Персона. Наследуется от Базовой модели.
    Хранит Информацию о запрашиваемых объектак, а именно:
    Их id, имя, тип объекта поиска, дату запроса и номер
    запроса(создаётся автоматически) и пользователя(
    в нём нет никакой практической пользы, не считая того,
    что без него всё время всплывает ошибка - error: [NOT NULL constraint failed]
    ).
    '''
    request_id = pw.AutoField()
    created_at = pw.DateField(default=datetime.now())
    user = pw.ForeignKeyField(Person, backref='history')
    info_type = pw.TextField()
    object_id = pw.IntegerField()
    object_name = pw.TextField()


