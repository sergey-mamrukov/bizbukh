from models import db, Client, Event, Eventready, Eventstatus


# получить всех клиетов
def get_all_clients():
    return Client.query.all()

# получить определенного клиента по id
def get_client(clientid):
    return Client.query.get(clientid)

# получить все события
def get_events():
    return Event.query.all()

# получить все статусы
def get_eventstatuses():
    return Eventstatus.query.all()

# получить все выполненные события
def get_eventredy_all():
    return Eventready.query.all()


# получить все выполненные события
def get_eventredy_forclient(client):
    return Eventready.query.filter_by(client = client)



