from models import db, Opf


# получить орг. прав. форму по id
def get_opf(id):
    return  Opf.query.get(id)

# получить все орг. прав. формы
def get_all_opf():
    return Opf.query.all()