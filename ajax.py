from client_events import get_event_on_client_day
from eventstatus_helper import *
from client_events import get_client_event_all,get_status_event,get_client_personalevent_date_all,get_client_personalevent_all








# получение информации о клиенте и массива с событиями в формате json
def get_client_info(client):
    client_name = client.client_name
    client_id = client.id
    datazp = client.client_datazp
    dataavansa = client.client_dataavansa
    opf = client.opf.opf_name

    clientevents = get_client_event_all(client)
    pevents = get_client_personalevent_all(client)


    events = []
    result = None
    for event in clientevents:
        if not get_status_event(client, event) == st_notready():
            e = {"nameevent":event.event_name,
                 "shortname":event.short_name,
                 "eventid":str(event.id),
                 "datastart":str(event.event_data_start),
                 "dataend":str(event.event_data_end),
                 "status":str(get_status_event(client,event)),
                 "type_event":event.type_event,
                 "ispersonal":False}

            events.append(e)


    if pevents:
        for event in pevents:
            e = {"nameevent": event.event_name,
                  "eventid": str(event.id),
                  "dataend": str(event.event_data_end),
                  "status": event.status,
                  "ispersonal":True,
                  "clientid":str(client_id)}

            events.append(e)


    result = { "clientname":client_name,
                   "client_id":client_id,
                   "datazp":datazp,
                   "dataavansa":dataavansa,
                   "opf":opf,
                   "events":events}

    return result


# получение информации о клиенте и событий на определенную дату
def get_client_info_on_date(client, date):
    client_name = client.client_name
    client_id = client.id
    datazp = client.client_datazp
    dataavansa = client.client_dataavansa
    opf = client.opf.opf_name

    clientevents = get_event_on_client_day(client,date)
    pevents = get_client_personalevent_date_all(client,date)

    events = []
    result = None
    for event in clientevents:
        if not get_status_event(client,event) == st_notready():
            e = {"nameevent":event.event_name,
                 "eventid":str(event.id),
                 "datastart":str(event.event_data_start),
                 "dataend":str(event.event_data_end),
                 "status":str(get_status_event(client,event)),
                 "ispersonal":False}

            events.append(e)


    if pevents:
        for event in pevents:
                e = {"nameevent":event.event_name,
                     "eventid":str(event.id),
                     "dataend":str(event.event_data_end),
                     "status":  event.status,
                     "ispersonal":True,
                     "clientid":str(client_id)}

                events.append(e)


    result = { "clientname":client_name,
                "client_id":client_id,
                "datazp":datazp,
                "dataavansa":dataavansa,
                "opf":opf,
                "events":events}

    return result


def get_event_info(event):
    result = {  "eventname":event.event_name,
                "shortname": event.short_name,
                "datastart":str(event.event_data_start),
                "dataend":str(event.event_data_end),
                "eventid":event.id,
                "type_event":event.type_event,
                }

    return result

def get_zp_info(fullname, shortname, dataend):
    result = {  "eventname":fullname,
                "shortname": shortname,
                "dataend":dataend,
                }

    return result







