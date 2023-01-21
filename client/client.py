from flask import Blueprint, url_for, render_template, redirect, request

from client_helper import addClient, editClient, delClient, get_all_clients, get_client
from opf_helper import get_all_opf, get_opf
from tag_helper import get_all_tag
from nalog_helper import get_all_nalog, get_nalog

from event_helper import getClientEvents, geteventok, addEventOk


client = Blueprint('client', __name__, template_folder='templates')


# Вывод списка организаций на странице
@client.route('/')
def clientlist():
    clients = get_all_clients()
    return render_template("client/client_list.html",clients = clients)

# Вывод карточки организации
@client.route('/<int:clientid>')
def clientcart(clientid):
    client = get_client(clientid)
    events = getClientEvents(client)

    print(client.tag)
    # status = get_eventstatuses()

    # addEventOk(client,events[0],status[0])
    # geteventok()
    # geteventok()

    return render_template('client/client_cart.html', client=client, events=events)


# Добавление организации
@client.route('/addclient', methods = ['GET', 'POST'])
def addclient():

    # формируем списки с параметрами
    tags = get_all_tag()
    nalogs = get_all_nalog()
    opfs = get_all_opf()


    # парсим форму
    clientTags = []

    for tag in tags:
        if (request.form.get(f'checktag_{tag.id}')) == 'on':
            clientTags.append(tag)

    client_name = request.form.get('name')
    client_description = request.form.get('description')
    client_inn = request.form.get('inn')

    client_datazp = request.form.get('datazp')
    client_dataavansa = request.form.get('dataavans')

    opf = get_opf(request.form.get('radioopf'))
    nalog = get_nalog(request.form.get('radionalog'))

    # обрабатываем метод post
    if request.method == 'POST':
        try:
            addClient(client_name,client_description,client_inn, client_datazp,client_dataavansa,opf,nalog,clientTags)
            # редиректим на список клиентов
            return redirect(url_for('client.clientlist'))
        except: print('error')

    return render_template("client/add_client.html", tags = tags, nalogs=nalogs, opfs =opfs)

# Редактирование организации
@client.route('/clientedit/<int:clientid>', methods = ['GET', 'POST'])
def clientedit(clientid):
    # ищем клиента по id
    client = get_client(clientid)

    tags = get_all_tag()
    nalogs = get_all_nalog()
    opfs = get_all_opf()

    # парсим форму
    clientTags = []

    for tag in tags:
        if (request.form.get(f'checktag_{tag.id}')) == 'on':
            clientTags.append(tag)

    client_name = request.form.get('name')
    client_description = request.form.get('description')
    client_inn = request.form.get('inn')

    client_datazp = request.form.get('datazp')
    client_dataavansa = request.form.get('dataavans')

    opf = get_opf(request.form.get('radioopf'))
    nalog = get_nalog(request.form.get('radionalog'))

    if request.method == 'POST':
        try:
            editClient(client, client_name, client_description, client_inn, client_datazp, client_dataavansa, opf, nalog,
                      clientTags)
            # редиректим на список клиентов
            return redirect(url_for('client.clientlist'))
        except:
            print('error')

    return render_template("client/edit_client.html", tags = tags, nalogs=nalogs, opfs =opfs, client=client)

# Удаление организации
@client.route('/clientdel/<int:clientid>/')
def clientdel(clientid):
    client = get_client(clientid)
    delClient(client)
    return redirect(url_for('client.clientlist'))

