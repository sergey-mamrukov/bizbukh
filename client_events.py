import datetime

from event_helper import get_event_for_opf, get_event_for_nalog, get_event_for_tags
from eventready_helper import get_ready, check_event_ready, change_status
from eventstatus_helper import st_ok,st_notready,st_proof, st_no
from client_helper import get_client_for_tags,get_client_for_nalog,get_client_for_opf


# возвращает список всех событий для клиента
def get_client_event_all(client):
    opf = client.opf
    nalog = client.nalog
    tags = client.tag

    events = []

    events.extend(get_event_for_opf(opf))
    events.extend(get_event_for_nalog(nalog))
    events.extend(get_event_for_tags(tags))

    result = list(set(events))
    return result

# возвращает список клиентов ля события
def get_event_clients_all(event):
    opf = event.opf
    nalog = event.nalog
    tags = event.tag

    clients = []

    clients.extend(get_client_for_opf(opf))
    clients.extend(get_client_for_nalog(nalog))
    clients.extend(get_client_for_tags(tags))
    # print(clients)
    result = list(set(clients))
    # print(result)

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
            if event == revent.event:
                return revent.status

    else:
        change_status(client,event,st_no())
        return st_no()

# Получить все события на определенную дату по клиенту
def get_event_on_client_day(client, data):
    allevent = get_client_event_all(client)
    result = []
    for event in allevent:
        if str(event.event_data_end) == str(data):
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
def get_event_on_client_month(client, data):
    allevent = get_client_event_all(client)
    result = []
    for event in allevent:
        if event.event_data_end == data:
            result.append(event)
    return result



