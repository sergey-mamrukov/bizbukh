from client_events import get_event_on_client_day
from eventstatus_helper import st_no,st_ok,st_notready,st_proof
from client_events import get_client_event_all,get_status_event,get_client_personalevent_date_all,get_client_personalevent_all

from dadata import Dadata
from config import token_dadata, secret_datdata



# получение информации о клиенте и массива с событиями в формате json
def get_client_info(client):
    client_name = client.client_name
    client_id = client.id
    # datazp = client.client_datazp
    # dataavansa = client.client_dataavansa
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
                   # "datazp":datazp,
                   # "dataavansa":dataavansa,
                   "opf":opf,
                   "events":events}

    return result


# получение информации о клиенте и событий на определенную дату
def get_client_info_on_date(client, date):
    client_name = client.client_name
    client_id = client.id
    # datazp = client.client_datazp
    # dataavansa = client.client_dataavansa
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
                # "datazp":datazp,
                # "dataavansa":dataavansa,
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



def get_info_on_inn(clientinn):
    error = False

    with Dadata(token_dadata, secret_datdata) as dadata:
        result = dadata.find_by_id("party", clientinn)

        if result:
            type = result[0]['data']['type']
            inn = result[0]['data']['inn']

            ogrn = result[0]['data']['ogrn']
            full_name = result[0]['data']['name']['full_with_opf']
            short_name = result[0]['data']['name']['short_with_opf']
            address = result[0]['data']['address']['value']

            persone_name = ''
            persone_post = ''
            kpp = ''

            if result[0]['data']['type'] == "LEGAL":
                persone_name = result[0]['data']['management']['name']
                persone_post = result[0]['data']['management']['post']
                kpp = result[0]['data']['kpp']
            if result[0]['data']['type'] == "INDIVIDUAL":
                persone_name = f"{result[0]['data']['fio']['surname']} {result[0]['data']['fio']['name']} {result[0]['data']['fio']['patronymic']}"
        else:
            type = ''
            inn = ''
            ogrn = ''
            full_name = ''
            short_name = ''
            address = ''
            persone_name = ''
            persone_post = ''
            kpp = ''
            error = True

    j = {
            'type': type,
            'inn': inn,
            'kpp': kpp,
            'ogrn': ogrn,
            'full_name': full_name,
            'short_name': short_name,
            'address': address,
            'persone_name': persone_name,
            'persone_post': persone_post,
            'error': error}

    return j










