import datetime

from event_helper import get_all_event
from eventready_helper import get_ready, check_event_ready, change_status_event, add_eventready
from eventstatus_helper import st_ok,st_notready,st_proof, st_no
from client_helper import get_client_for_tags,get_client_for_nalog,get_client_for_opf, get_all_clients

from personalevent_helper import get_personal_event_all, get_personal_event_date_all,get_personal_event_date_month



# возвращает список всех статичных событий для клиента
def get_client_event_all(client):
    opf = client.opf
    nalog = client.nalog
    tags = client.tag

    allevents = get_all_event()

    result = []

    for event in allevents:
        if(opf in event.opf or nalog in event.nalog):
            result.append(event)
        for tag in tags:
            if tag in event.tag:
                result.append(event)

    return result




# возвращает список персональных событий для клиента
def get_client_personalevent_all(client):
    p_events = get_personal_event_all(client)
    return p_events

# возвращает список персональных событий для клиента на дату
def get_client_personalevent_date_all(client,date):
    p_events = get_personal_event_date_all(client,date)
    # print(f'pevents on date: {p_events}')
    return p_events


# возвращает список персональных событий для клиента на месяц
def get_client_personalevent_date_month(client,date):
    p_events = get_personal_event_date_month(client,date)
    return p_events

# возвращает список клиентов для события
def get_event_clients_all(event):
    opf = event.opf
    nalog = event.nalog
    tags = event.tag

    allclients = get_all_clients()
    result = []
    for client in allclients:
        if client.opf in opf or client.nalog in nalog:
            result.append(client)
        for tag in client.tag:
            if tag in tags:
                result.append(client)

    return result




# возвращает список актуальных событий (которые не выполнены, т.е имеют статус "не выполнено" или нет в таблице выпоненных)
def get_client_event_actual(client):
    event_no = get_client_event_no(client)
    all_event = get_client_event_all(client)
    result = []

    for event in all_event:
        if check_event_ready(client,event):
            if event in event_no:
                result.append(event)
        else:
            result.append(event)
    return result


# возвращает список выполненных событий (которые имеют статус "выполнено" или "подтверждено")
def get_client_event_ready(client):
    ready = []
    ready_event = get_ready(client)

    for event in ready_event:
        if event.status == st_ok() or event.status == st_proof():
            ready.append(event.event)
    return ready


# возвращает список не выполненных событий (которые имеют статус "не выполнено")
def get_client_event_no(client):
    ready = []
    ready_event = get_ready(client)

    for event in ready_event:
        if event.status == st_no():
            ready.append(event.event)
    return ready


# возвращает список не выполняемых событий
def get_client_event_notready(client):
    notready = []
    ready_event = get_ready(client)

    for event in ready_event:
        if event.status ==  st_notready():
            notready.append(event.event)
    return notready

# возвращает статус события
def get_status_event(client,event):
    readyevent = get_ready(client)

    if readyevent:
        for revent in readyevent:
            if revent.event == event:
                return revent.status

        change_status_event(client, event, st_no())
        return st_no()

    else:
        change_status_event(client,event,st_no())
        return st_no()




# Получить все события на определенную дату по клиенту
def get_event_on_client_day(client, data):
    allevent = get_client_event_all(client)
    result = []

    for event in allevent:
        if str(event.event_data_end) == str(data):
            result.append(event)
    return result

# Получить все события на определенный месяц (год-месяц) по клиенту
def get_event_on_client_month(client, data):
    allevent = get_client_event_all(client)
    result = []

    for event in allevent:
        if str(data) in str(event.event_data_end):
            result.append(event)
    return result







# Получить выпоненные событий на дату по клиенту
def get_eventok_on_client_day(client, data):
    allevent = get_event_on_client_day(client,data)
    readyevent = get_client_event_ready(client)
    result = []

    if allevent:
        for event in allevent:
            if event in readyevent:
                result.append(event)

    else: return result

    return result


# Получить все события на определенный месяц по клиенту
# def get_event_on_client_month(client, data):
#     allevent = get_client_event_all(client)
#     result = []
#     for event in allevent:
#         if event.event_data_end == data:
#             result.append(event)
#     return result



