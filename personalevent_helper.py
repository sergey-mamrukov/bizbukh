from models import db, PersonalEvent

from eventstatus_helper import *

# получить персональное событие по id
def get_personal_event(id):
    return PersonalEvent.query.get(id)

# получить все персональные события у клиента
def get_personal_event_all(client):
    return PersonalEvent.query.filter(PersonalEvent.client == client).all()

# получить все события по зп у клиента
def get_personal_zp_event_all(client):
    return PersonalEvent.query.filter(PersonalEvent.client == client, PersonalEvent.is_zp == True).all()

# получить все персональные события у клиента на определенную дату
def get_personal_event_date_all(client, date):
    return PersonalEvent.query.filter(PersonalEvent.client == client, PersonalEvent.event_data_end == date).all()

# получить все персональные события у клиента на определенный  месяц
def get_personal_event_date_month(client, date):
    events = PersonalEvent.query.filter(PersonalEvent.client == client).all()
    print(f"get_personal_event_date_month: {events}")
    result = []
    for event in events:
        print(f'event data- {event.event_data_end}, data - {date}')
        if str(date) in str(event.event_data_end):

            result.append(event)

    print(f"get_personal_event_date_month (result): {result}")
    return result


# создать персональное событие
def addPersonalEvent(client,name,data_end):
    pEvent = PersonalEvent()

    pEvent.event_name = name
    pEvent.client = client
    pEvent.status = st_no()
    pEvent.event_data_end = data_end


    db.session.add(pEvent)
    db.session.commit()


def addzpEvent(client, name,sortname,data_end):
    zpevent = PersonalEvent()

    zpevent.client = client
    zpevent.event_name = name
    zpevent.short_name = sortname
    zpevent.event_data_end = data_end
    zpevent.is_zp = True
    zpevent.status = st_no()

    db.session.add(zpevent)
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
