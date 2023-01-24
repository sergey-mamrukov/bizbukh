from event_helper import get_event_for_opf, get_event_for_nalog, get_event_for_tags
from eventready_helper import get_ready, check_event_ready
from eventstatus_helper import st_ok,st_notready,st_proof, st_no


# возвращает список всех событий для клиента
def get_client_event_all(client):
    opf = client.opf
    nalog = client.nalog
    tags = client.tag

    events = []

    events.extend(get_event_for_opf(opf))
    events.extend(get_event_for_nalog(nalog))
    events.extend(get_event_for_tags(tags))

    return events


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