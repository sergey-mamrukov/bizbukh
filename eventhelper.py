from models import db, Event,Client
from db_helper import get_client, get_events


# Возвращает список всех событий по айди клиента
def getEvents(clientid):
    client = Client.query.get(clientid)

    clienttags = []
    events = []

    for ttag in client.tag:
        clienttags.append(ttag)

    for tag in clienttags:
        for t in tag.events:
            events.append(t)

    for nalog in client.sysnalog:
        for n in nalog.events:
            events.append(n)

    for opf in client.opf:
        for o in opf.events:
            events.append(o)

    return set(events)


# Возвращает список всех событий по айди клиента
def getEventsbyobject(client):
    clienttags = []
    events = []

    for ttag in client.tag:
        clienttags.append(ttag)

    for tag in clienttags:
        for t in tag.events:
            events.append(t)

    for nalog in client.sysnalog:
        for n in nalog.events:
            events.append(n)

    for opf in client.opf:
        for o in opf.events:
            events.append(o)

    return set(events)

def getCountEventsonDate(date, clientid):
    events = getEvents(clientid)
    count =0

    for event in events:
        print(event.event_data_start)
        print(date)
        if event.event_data_start == date:
            count += 1

    return count
