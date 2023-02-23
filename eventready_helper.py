from models import db, Eventready
from eventstatus_helper import *

# проверяет есть ли запись в таблице выполненных событие
def check_event_ready(client, event):
    allready = get_ready(client)
    if allready:
        for ready in allready:
            if ready.event == event:
                return True
    else: return False

# возвращает объект готового события по клиенту и событию
def get_ready_event(client, event):
    if check_event_ready(client,event):
        allready = get_ready(client)
        for ready in allready:
            if ready.event == event:
                return ready
    else: return None


# добавляет в таблицу Eventready запись о выполненном событии
def add_eventready(client, event, status):
    if not check_event_ready(client,event):
        ready = Eventready()
        ready.event = event
        ready.status = status
        ready.client = client

        db.session.add(ready)
        db.session.commit()

    else: print ('событие в таблце')

# ищет и удаляет все записи в таблице Eventready
def del_eventready(client):
    eventreadyes = Eventready.query.filter(Eventready.client_id == client.id).all()
    for e in eventreadyes:
        db.session.delete(e)
    db.session.commit()


# меняет статус события
def change_status_event(client, event, status):
    ready = get_ready(client)

    if ready:
        for r in ready:
            if r.event == event:
                r.status = status
                db.session.commit()
            else: add_eventready(client,event,status)

    else: add_eventready(client,event, st_no())


def get_ready(client):
    return Eventready.query.filter_by(client = client).all()

