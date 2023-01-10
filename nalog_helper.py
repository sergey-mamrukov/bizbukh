from models import db, Systnalog


# получить систему налогообложения по id
def get_nalog(id):
    return  Systnalog.query.get(id)

# получить все системы налогообложения
def get_all_nalog():
    return Systnalog.query.all()