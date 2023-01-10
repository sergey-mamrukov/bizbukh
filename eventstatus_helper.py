from models import db, Eventstatus


# получить статус события по id
def get_eventstatus(id):
    return  Eventstatus.query.get(id)

# получить все статусы событий
def get_all_eventstatus():
    return Eventstatus.query.all()