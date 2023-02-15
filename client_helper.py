from models import db, Client


# add new client
def addClient(client_name,
              client_description,
              client_inn,
              client_datazp,
              client_dataavansa,
              opf,
              nalog,
              tags):

      # создаем клиента
      client = Client()

      # проверки и занесение параметров
      if client_name:
            client.client_name = client_name
      else: client.client_name = "error name"

      if client_inn:
            client.client_inn = client_inn
      else: client.client_inn = '0000000000'

      if client_description:
            client.client_description = client_description
      else:
            client.client_description = ""

      if client_dataavansa and client_dataavansa != 0:
            client.client_dataavansa = client_dataavansa
      else:
            client.client_dataavansa = 0

      if client_datazp and client_datazp != 0:
            client.client_datazp = client_datazp
      else:
            client.client_datazp = 0

      client.opf = opf
      client.nalog = nalog
      client.tag[:] = tags

      # добавление клиента в базу
      db.session.add(client)
      db.session.commit()

# edit client
def editClient(client, client_name,
              client_description,
              client_inn,
              client_datazp,
              client_dataavansa,
              opf,
              nalog,
              tags):

      # обнуление тэгов, опф и налога
      client.opf = None
      client.tag[:] = []
      client.nalog = None

      # проверки и занесение параметров
      if client_name:
            client.client_name = client_name
      else:
            client.client_name = "error name"

      if client_inn:
            client.client_inn = client_inn
      else:
            client.client_inn = '0000000000'

      if client_description:
            client.client_description = client_description
      else:
            client.client_description = ""

      if client_dataavansa and client_dataavansa != 0:
            client.client_dataavansa = client_dataavansa
      else:
            client.client_dataavansa = 0

      if client_datazp and client_datazp != 0:
            client.client_datazp = client_datazp
      else:
            client.client_datazp = 0

      client.opf = opf
      client.nalog = nalog
      client.tag[:] = tags

      db.session.commit()


# del client
def delClient(client):
      db.session.delete(client)
      db.session.commit()


# получить всех клиетов
def get_all_clients():
    return Client.query.all()

# получить определенного клиента по id
def get_client(clientid):
    return Client.query.get(clientid)


# получить всех клиентов по ОПФ
def get_client_for_opf(opf):
    clients = []
    for client in get_all_clients():
        if client.opf in opf:
            clients.append(client)
    return clients


# получить событие по налогу
def get_client_for_nalog(nalog):
    clients = []
    for client in get_all_clients():
        if client.nalog in nalog :
            clients.append(client)

    return clients

# получить событие по тегу
def get_client_for_tags(tags):
    clients = []
    if tags:
        allclients = get_all_clients()
        for tag in tags:
            for client in allclients:
                if tag in client.tag:
                    clients.append(client)
    return clients