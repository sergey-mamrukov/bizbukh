from models import db, Event, PersonalEvent



# получить событие по id
def get_event(id):
    return Event.query.get(id)

# получить все события
def get_all_event():
    result = Event.query.all()
    print(result)
    return result



# получить события на определенную дату
def get_events_on_day(date):
    events = get_all_event()
    result = []
    for event in events:
        if str(event.event_data_end) == date:
            result.append(event)
    return result

# удалить событие
def delEvent(event):
    db.session.delete(event)
    db.session.commit()


# добавление события
def addEvent(event_name,
             data_start,
             data_end,
             tags,
             nalogs,
             opfs,
             typeevent,
             shortname):

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


    if typeevent:
        event.type_event = typeevent
    else:
        event.type_event = None

    if shortname:
        event.short_name = shortname
    else:
        event.short_name = None


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
             tags,
             nalogs,
             opfs,
             typeevent,
             shortname):



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

    if typeevent:
        event.type_event = typeevent
    else:
        event.type_event = None

    if shortname:
        event.short_name = shortname
    else:
        event.short_name = None

    event.tag[:] = tags
    event.opf[:] = opfs
    event.nalog[:] = nalogs

    db.session.commit()






