from database.utils.CRUD import CRUDInterface
from database.common.models import db, Person, History

db.connect()
db.create_tables([Person, History])


crud = CRUDInterface()


if __name__ == '__main__':
    crud()