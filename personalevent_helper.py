from models import db, PersonalEvent

from eventstatus_helper import *

# получить персональное событие по id
def get_personal_event(id):
    return PersonalEvent.query.get(id)

# получить все персональные события у клиента
def get_personal_event_all(client):
    return PersonalEvent.query.filter(PersonalEvent.client == client).all()

# получить все персональные события у клиента а определенную дату
def get_personal_event_date_all(client, date):
    return PersonalEvent.query.filter(PersonalEvent.client == client, PersonalEvent.event_data_end == date).all()


# создать персональное событие
def addPersonalEvent(client,name,data_end):
    pEvent = PersonalEvent()

    pEvent.event_name = name
    pEvent.client = client
    pEvent.status = st_no()
    pEvent.event_data_end = data_end


    db.session.add(pEvent)
    db.session.commit()


# редактирвоать персональное событие
def editPersonalEvent(pevent, name, data_end):
    pevent.event_name = name
    pevent.event_data_end = data_end

    db.session.commit()

# редактирвоать персональное событие
def changestatusPersonalEvent(pevent,status):
    pevent.status = status

    db.session.commit()

# удалить персональное событие
def delPersonalEvent(pevent):
    db.session.delete(pevent)
    db.session.commit()
