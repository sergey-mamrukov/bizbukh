from flask import Blueprint, url_for, render_template, redirect, request,abort

from client_helper import addClient, editClient, delClient, get_all_clients, get_client
from opf_helper import get_all_opf, get_opf
from tag_helper import get_all_tag
from nalog_helper import get_all_nalog, get_nalog
from event_helper import get_event

from client_events import get_client_event_all,get_client_event_ready, get_client_event_actual, get_client_event_notready,get_status_event
from eventready_helper import change_status_event
from eventstatus_helper import st_ok,st_proof,st_notready, st_no
from flask_login import current_user
from models import db


client = Blueprint('client', __name__, template_folder='templates')


# Вывод списка организаций на странице
@client.route('/')
def clientlist():
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    clients = get_all_clients()
    return render_template("client/client_list.html",clients = clients)

# Вывод карточки организации
@client.route('/<int:clientid>')
def clientcart(clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))


    client = get_client(clientid)

    # client.user.append(current_user)
    # db.session.commit()


    all_events = []
    for event in get_client_event_all(client):
        all_events.append([event,get_status_event(client,event)])


    ready_events = get_client_event_ready(client)
    notready_events = get_client_event_notready(client)
    actual_events = get_client_event_actual(client)


    return render_template('client/client_cart.html', client=client, all_events = all_events,
                           ready_events = ready_events, notready_events = notready_events,
                           actual_events = actual_events)


# Добавление организации
@client.route('/addclient', methods = ['GET', 'POST'])
def addclient():
    if current_user.is_anonymous:
        return redirect(url_for("login"))

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
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    # ищем клиента по id
    client = get_client(clientid)

    if current_user not in client.user:
        # pass
        abort(404)

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
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    delClient(client)
    return redirect(url_for('client.clientlist'))






@client.route('/eventok/<int:eventid>/<int:clientid>')
def eventok(eventid, clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    event = get_event(eventid)
    status = st_ok()
    change_status_event(client,event,status)
    return redirect(url_for('client.clientcart',clientid = clientid))



@client.route('/eventno/<int:eventid>/<int:clientid>')
def eventno(eventid, clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    event = get_event(eventid)
    change_status_event(client,event, st_no())
    return redirect(url_for('client.clientcart',clientid = clientid))


@client.route('/eventproof/<int:eventid>/<int:clientid>')
def eventproof(eventid, clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    event = get_event(eventid)
    status = st_proof()
    change_status_event(client,event,status)

    return redirect(url_for('client.clientcart',clientid = clientid))

@client.route('/eventnotready/<int:eventid>/<int:clientid>')
def eventnotready(eventid, clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    event = get_event(eventid)
    status = st_notready()
    change_status_event(client,event,status)

    return redirect(url_for('client.clientcart',clientid = clientid))