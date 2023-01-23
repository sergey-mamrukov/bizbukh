from client_helper import get_client
from event_helper import get_event_for_opf, get_event_for_nalog, get_event_for_tags
from eventready_helper import get_ready,change_status, del_eventready, check_event_ready
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
    event_notready = get_client_event_notready(client)
    event_ready = get_client_event_ready(client)
    event_no = get_client_event_no(client)
    all_event = get_client_event_all(client)
    result = []
    print (f'ready - {event_ready}')
    print (f'notready - {event_notready}')
    print (f'event no - {event_no}')
    for event in all_event:
        if check_event_ready(client,event):
            print ('check  true')
            if event in event_no:
                print ('event in NO')
                result.append(event)
        else:
            result.append(event)

    print (f'result - {result}')


    # print(f'notready = {not_ready_event}')
    # print(f'readyok = {ready_event}')
    # print(f'allevent = {all_event}')
    # print(f'result = {result}')

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


# возвращает список событий клиента на определенную дату

# возвращает просроченные события



# меняет статус события клиента (если событие не выполненно, добавляет в таблицу выполненных,
# если статус меняется на "не выполнено", удаляет из таблицы выполненных, если добавляется статус "не выполняется", добавляет запись в таблицу,
# все это дополнительно проверяется
