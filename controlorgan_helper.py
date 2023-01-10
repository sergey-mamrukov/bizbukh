from models import db,Controlorgan

# получить контролирующего органа по id
def get_controlorgan(id):
    return  Controlorgan.query.get(id)

# получить все контролирующие органы
def get_all_controlorgan():
    return Controlorgan.query.all()