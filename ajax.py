from client_events import get_client_event_all,get_status_event,get_event_on_client_day
from eventstatus_helper import st_notready

# получение информации о клиенте и массива с событиями в формате json
def get_client_info(client):
    client_name = client.client_name
    client_id = client.id
    datazp = client.client_datazp
    dataavansa = client.client_dataavansa
    opf = client.opf.opf_name
    # systalog = client.nalog.nalog_name

    clientevents = get_client_event_all(client)

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
                 "type_event":event.type_event}

            events.append(e)

        result = { "clientname":client_name,
                   "client_id":client_id,
                   "datazp":datazp,
                   "dataavansa":dataavansa,
                   "opf":opf,
                   # "sysnalog":systalog,
                   "events":events}

    return result


# получение информации о клиенте и событий на определенную дату
def get_client_info_on_date(client, date):
    client_name = client.client_name
    client_id = client.id
    datazp = client.client_datazp
    dataavansa = client.client_dataavansa
    opf = client.opf.opf_name
    # systalog = client.nalog.nalog_name

    clientevents = get_event_on_client_day(client,date)

    events = []
    result = None
    for event in clientevents:
        if not get_status_event(client,event) == st_notready():
            e = {"nameevent":event.event_name,
                 "eventid":str(event.id),
                 "datastart":str(event.event_data_start),
                 "dataend":str(event.event_data_end),
                 "status":str(get_status_event(client,event))}

            events.append(e)

    result = { "clientname":client_name,
                "client_id":client_id,
                "datazp":datazp,
                "dataavansa":dataavansa,
                "opf":opf,
                # "sysnalog":systalog,
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





