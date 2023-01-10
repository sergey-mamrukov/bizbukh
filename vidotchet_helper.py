from models import db, Vidotchet


# получить вид отчетности по id
def get_vidotchet(id):
    return  Vidotchet.query.get(id)

# получить все виды отчетности
def get_all_vidotchet():
    return Vidotchet.query.all()