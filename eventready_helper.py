from models import db, Eventready
from eventstatus_helper import get_eventstatus,get_all_eventstatus
from eventstatus_helper import st_ok,st_proof,st_notready


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

# ищет и удаляет запись в таблице Eventready запись о выполненном событии
def del_eventready(client,event):
    if check_event_ready(client,event):
        ready = get_ready_event(client,event)
        if ready:
            db.session.delete(ready)
            db.session.commit()
    else: print ('события нет в таблице')


# меняет статус события
def change_status(client, event, status):

    ready = get_ready(client)

    if ready:
        for r in ready:
            if r.event == event:
                r.status = status
                db.session.commit()
            else: add_eventready(client,event,status)

    else: add_eventready(client,event,status)


def get_ready(client):
    return Eventready.query.filter_by(client = client).all()

