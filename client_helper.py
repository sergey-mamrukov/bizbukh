from models import db, Client
from eventready_helper import del_eventready
from flask_login import current_user


# add new client
def addClient(data):

      # создаем клиента
      client = Client()

      client.company = data['company']
      client.user.append(current_user)

      client.client_name = data['client_name']
      client.client_description = data['client_description']

      if data['opf']: client.opf = data['opf']
      else: client.opf = None

      if data['clientTags']: client.tag[:] = data['clientTags']
      else: client.tag[:] = []

      if data['nalog']: client.nalog = data['nalog']
      else: client.nalog = None

      client.user[:] = data['clientUsers']

      client.client_fullname = data['client_fullname']
      client.client_shortname = data['client_shortname']
      client.client_uraddress = data['client_uraddress']
      client.client_pochtaddress = data['client_pochtaddress']
      client.client_kpp = data['client_kpp']
      client.client_inn = data['client_inn']
      client.client_ogrn = data['client_ogrn']
      client.client_director = data['client_director']
      client.client_osnovanie = data['client_osnovanie']


      client.client_bank_name = data['client_bank_name']
      client.client_bank_rs = data['client_bank_rs']
      client.client_bank_ks = data['client_bank_ks']
      client.client_bank_bik = data['client_bank_bik']

      client.client_contact_name = data['client_contact_name']
      client.client_contact_phone = data['client_contact_phone']
      client.client_contact_email = data['client_contact_email']


      # добавление клиента в базу
      db.session.add(client)
      db.session.commit()



# edit client
def editClient(data):

    client = data['client']

    client.client_name = data['client_name']
    client.client_description = data['client_description']

    if data['opf']: client.opf = data['opf']
    else: client.opf = None

    if data['clientTags']: client.tag[:] = data['clientTags']
    else: client.tag[:] = []

    if data['nalog']: client.nalog = data['nalog']
    else: client.nalog = None

    client.user[:] = data['clientUsers']

    client.client_fullname = data['client_fullname']
    client.client_shortname = data['client_shortname']
    client.client_uraddress = data['client_uraddress']
    client.client_pochtaddress = data['client_pochtaddress']
    client.client_kpp = data['client_kpp']
    client.client_inn = data['client_inn']
    client.client_ogrn = data['client_ogrn']
    client.client_director = data['client_director']
    client.client_osnovanie = data['client_osnovanie']

    client.client_bank_name = data['client_bank_name']
    client.client_bank_rs = data['client_bank_rs']
    client.client_bank_ks = data['client_bank_ks']
    client.client_bank_bik = data['client_bank_bik']

    client.client_contact_name = data['client_contact_name']
    client.client_contact_phone = data['client_contact_phone']
    client.client_contact_email = data['client_contact_email']

    db.session.commit()


# del client
def delClient(client):
      del_eventready(client)
      client.company = None
      # client.user[:] = []
      # db.session.commit()

      db.session.delete(client)
      db.session.commit()


# получить всех клиетов
def get_all_clients():
    # return Client.query.all()

    clients = Client.query.filter(Client.company == current_user.company).all()
    result = []
    for client in clients:
        if current_user in client.user or current_user.possition == "admin":
            result.append(client)
    return result

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

# def getClentsForCompany(company):
#     clients = get_all_clients()
#     return clients