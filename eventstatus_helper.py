from models import db, Eventstatus


# получить статус события по id
def get_eventstatus(id):
    return  Eventstatus.query.get(id)

# получить все статусы событий
def get_all_eventstatus():
    return Eventstatus.query.all()

# вернет статус "выполнено"
def st_ok():
    return get_eventstatus(1)

# вернет статус "подтверждено"
def st_proof():
    return get_eventstatus(2)

# вернет статус "не выполняется"
def st_notready():
    return get_eventstatus(3)

# вернет статус "не выполнено"
def st_no():
    return get_eventstatus(4)
