from models import db, Event,Client, Eventready


# получить событие по id
def get_event(id):
    return Event.query.get(id)

# получить все события
def get_all_event():
    return Event.query.all()


# удалить событие
def delEvent(event):
    db.session.delete(event)
    db.session.commit()


# добавление события
def addEvent(event_name,
             data_start,
             data_end,
             controlorgan,
             vidotchet,
             tags,
             nalogs,
             opfs):

    event = Event()

    if event_name:
        event.event_name = event_name
    else: event.event_name = "name error"

    if data_start and data_end and data_start <= data_end:
        event.event_data_start = data_start
        event.event_data_end = data_end
    else:
        event.event_data_start = None
        event.event_data_end = None


    if controlorgan:
        event.controlorgan = controlorgan
    else:
        event.controlorgan = None


    if vidotchet:
        event.vidotchet = vidotchet
    else: event.vidotchet = None


    event.tag[:] = tags
    event.opf[:] = opfs
    event.nalog[:] = nalogs

    db.session.add(event)
    db.session.commit()



# редактирование события
def editEvent(event,
             event_name,
             data_start,
             data_end,
             controlorgan,
             vidotchet,
             tags,
             nalogs,
             opfs):



    event.tag[:] = []
    event.opf[:] = []
    event.nalog[:] = []

    if event_name:
        event.event_name = event_name
    else:
        event.event_name = "name error"

    if data_start and data_end and data_start <= data_end:
        event.event_data_start = data_start
        event.event_data_end = data_end
    else:
        event.event_data_start = None
        event.event_data_end = None

    if controlorgan:
        event.controlorgan = controlorgan
    else:
        event.controlorgan = None

    if vidotchet:
        event.vidotchet = vidotchet
    else:
        event.vidotchet = None

    event.tag[:] = tags
    event.opf[:] = opfs
    event.nalog[:] = nalogs

    db.session.commit()



















# Возвращает список всех событий по айди клиента
def getEvents(clientid):
    client = Client.query.get(clientid)

    clienttags = []
    events = []

    for tag in client.tag:
        clienttags.append(tag)

    for tag in clienttags:
        for t in tag.events:
            events.append(t)

    for nalog in client.nalog:
        for n in nalog.events:
            events.append(n)

    for opf in client.opf:
        for o in opf.events:
            events.append(o)

    return set(events)


# Возвращает список всех событий клиента
def getClientEvents(client):
    '''Возвращает список всех событий (Event) клиента (Client)'''
    clienttags = []
    events = []

    if client.tag:
        for tag in client.tag:
            clienttags.append(tag)

    if client.nalog:
        nalog = client.nalog
        for n in nalog.events:
            events.append(n)

    if client.opf:
        opf = client.opf
        for o in opf.events:
            events.append(o)

    for tag in clienttags:
        for t in tag.events:
            events.append(t)

    return set(events)
    # return events

def getCountEventsonDate(date, clientid):
    events = getEvents(clientid)
    count =0

    for event in events:
        print(event.event_data_start)
        print(date)
        if event.event_data_start == date:
            count += 1

    return count


def  geteventok():
    # eventredy = Eventready.query.all()
    # rr = eventredy[0]
    #
    # cl = rr.client
    # ev = rr.event
    # st = rr.status
    #
    #
    # print(cl.client_name)
    # print(ev.event_name)
    # print(rr.status.status_name)

    pass

def addEventOk(client, event, status):
    eventready = Eventready()
    eventready.event = event
    eventready.client = client
    eventready.status = status
    db.session.add(eventready)
    db.session.commit()


