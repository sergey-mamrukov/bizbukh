from models import db, Client, Event


# получить всех клиетов
def get_all_clients():
    return Client.query.all()

# получить определенного клиента по id
def get_client(clientid):
    return Client.query.get(clientid)

# получить все события
def get_events():
    return Event.query.all()
