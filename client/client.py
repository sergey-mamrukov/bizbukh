from flask import Blueprint, url_for, render_template, redirect, request,abort, flash

from client_helper import addClient, editClient, delClient, get_all_clients, get_client
from opf_helper import get_all_opf, get_opf
from tag_helper import get_all_tag
from nalog_helper import get_all_nalog, get_nalog
from event_helper import get_event

from client_events import get_client_event_all,get_client_event_ready, get_client_event_actual, get_client_event_notready, get_status_event
from eventready_helper import change_status_event
from eventstatus_helper import st_ok,st_proof,st_notready, st_no
from flask_login import current_user
from client_helper import getClientsForCompany
from user_helper import  getUsersForCompany
from tariff_helper import check_count_client



client = Blueprint('client', __name__, template_folder='templates')


# Вывод списка организаций на странице
@client.route('/')
def clientlist():
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    company = current_user.company
    count_clients_in_company = len(getClientsForCompany(company))

    clients = get_all_clients()
    return render_template("client/client_list.html",clients = clients, count_clients_in_company = count_clients_in_company, company=company)

@client.route('/<int:clientid>/zp')
def clientzp(clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)

    return render_template("client/client_zp.html", client = client)

# Вывод карточки организации
@client.route('/<int:clientid>')
def clientcart(clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))


    client = get_client(clientid)

    if current_user not in client.user and current_user.possition != "admin":
        abort(404)

    all_events = []
    for event in get_client_event_all(client):
        all_events.append([event,get_status_event(client,event)])


    ready_events = get_client_event_ready(client)
    notready_events = get_client_event_notready(client)
    actual_events = get_client_event_actual(client)


    return render_template('client/client_cart.html', client=client, all_events = all_events,
                           ready_events = ready_events, notready_events = notready_events,
                           actual_events = actual_events)


# Вывод карточки организации
@client.route('/<int:clientid>/events')
def clientevents(clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)

    if current_user.possition != "admin":
        abort(404)



    return render_template('client/client_events.html', client=client)










# Добавление организации
@client.route('/addclient', methods = ['GET', 'POST'])
def addclient():
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    if not check_count_client(current_user.company):
        flash("Ошибка добавления организации! Перейдите на другой тариф.")
        return redirect(url_for("client.clientlist"))

    # формируем списки с параметрами
    tags = get_all_tag()
    nalogs = get_all_nalog()
    opfs = get_all_opf()

    company = current_user.company
    users = getUsersForCompany(company)




    # парсим форму
    clientTags = []

    for tag in tags:
        if (request.form.get(f'checktag_{tag.id}')) == 'on':
            clientTags.append(tag)


    clientUsers = []

    for user in users:
        if (request.form.get(f'checkuser_{user.id}')) == 'on':
            clientUsers.append(user)

    opf = get_opf(request.form.get('radioopf'))
    nalog = get_nalog(request.form.get('radionalog'))

    client_name = request.form.get('name')
    client_description = request.form.get('description')

    # Реквизиты организации
    client_inn = request.form.get('client_inn')
    client_fullname = request.form.get('client_fullname')
    client_shortname = request.form.get('client_shortname')
    client_uraddress = request.form.get('client_uraddress')
    client_pochtaddress = request.form.get('client_pochtaddress')
    client_kpp = request.form.get('client_kpp')
    client_ogrn = request.form.get('client_ogrn')
    client_director = request.form.get('client_director')
    client_osnovanie = request.form.get('client_osnovanie')

    # Банковские реквизиты
    client_bank_name = request.form.get('client_bank')
    client_bank_bik = request.form.get('client_bik')
    client_bank_rs = request.form.get('client_rs')
    client_bank_ks = request.form.get('client_ks')

    # Контакты организации
    client_contact_name = request.form.get('client_name')
    client_contact_phone = request.form.get('client_phone')
    client_contact_email = request.form.get('client_email')

    data = {
        'client_inn':client_inn,
        'client_fullname':client_fullname,
        'client_shortname':client_shortname,
        'client_uraddress':client_uraddress,
        'client_pochtaddress':client_pochtaddress,
        'client_kpp':client_kpp,
        'client_ogrn':client_ogrn,
        'client_director':client_director,
        'client_osnovanie':client_osnovanie,
        'client_bank_name':client_bank_name,
        'client_bank_bik':client_bank_bik,
        'client_bank_rs':client_bank_rs,
        'client_bank_ks':client_bank_ks,
        'client_contact_name':client_contact_name,
        'client_contact_phone':client_contact_phone,
        'client_contact_email':client_contact_email,
        'client_name':client_name,
        'client_description':client_description,
        'opf':opf,
        'nalog':nalog,
        'clientTags':clientTags,
        'clientUsers':clientUsers,
        'company':company
        }

    # обрабатываем метод post
    if request.method == 'POST':
        # try:
            addClient(data)

            # редиректим на список клиентов
            return redirect(url_for('client.clientlist'))
        # except: print('error')

    return render_template("client/add_client.html", tags = tags, nalogs=nalogs, opfs =opfs, users = users)

# Редактирование организации
@client.route('/clientedit/<int:clientid>', methods = ['GET', 'POST'])
def clientedit(clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    # ищем клиента по id
    client = get_client(clientid)

    company = current_user.company
    users = getUsersForCompany(company)

    if current_user not in client.user and current_user.possition != "admin":
        abort(404)

    tags = get_all_tag()
    nalogs = get_all_nalog()
    opfs = get_all_opf()

    # парсим форму
    clientTags = []

    for tag in tags:
        if (request.form.get(f'checktag_{tag.id}')) == 'on':
            clientTags.append(tag)

    clientUsers = []

    for user in users:
        if (request.form.get(f'checkuser_{user.id}')) == 'on':
            clientUsers.append(user)


    opf = get_opf(request.form.get('radioopf'))
    nalog = get_nalog(request.form.get('radionalog'))


    client_name = request.form.get('name')
    client_description = request.form.get('description')

    # Реквизиты организации
    # Реквизиты организации
    client_inn = request.form.get('client_inn')
    client_fullname = request.form.get('client_fullname')
    client_shortname = request.form.get('client_shortname')
    client_uraddress = request.form.get('client_uraddress')
    client_pochtaddress = request.form.get('client_pochtaddress')
    client_kpp = request.form.get('client_kpp')
    client_ogrn = request.form.get('client_ogrn')
    client_director = request.form.get('client_director')
    client_osnovanie = request.form.get('client_osnovanie')

    # Банковские реквизиты
    client_bank_name = request.form.get('client_bank')
    client_bank_bik = request.form.get('client_bik')
    client_bank_rs = request.form.get('client_rs')
    client_bank_ks = request.form.get('client_ks')

    # Контакты организации
    client_contact_name = request.form.get('client_name')
    client_contact_phone = request.form.get('client_phone')
    client_contact_email = request.form.get('client_email')

    data = {
        'client_inn': client_inn,
        'client_fullname': client_fullname,
        'client_shortname': client_shortname,
        'client_uraddress': client_uraddress,
        'client_pochtaddress': client_pochtaddress,
        'client_kpp': client_kpp,
        'client_ogrn': client_ogrn,
        'client_director': client_director,
        'client_osnovanie': client_osnovanie,
        'client_bank_name': client_bank_name,
        'client_bank_bik': client_bank_bik,
        'client_bank_rs': client_bank_rs,
        'client_bank_ks': client_bank_ks,
        'client_contact_name': client_contact_name,
        'client_contact_phone': client_contact_phone,
        'client_contact_email': client_contact_email,
        'client_name': client_name,
        'client_description': client_description,
        'opf': opf,
        'nalog': nalog,
        'clientTags': clientTags,
        'clientUsers': clientUsers,
        'company': company,
        'client':client
    }



    if request.method == 'POST':
        try:
            editClient(data)
            # редиректим на список клиентов
            return redirect(url_for('client.clientlist'))
        except:
            print('error')

    return render_template("client/edit_client.html", tags = tags, nalogs=nalogs, opfs =opfs, client=client, users = users)

# Удаление организации
@client.route('/clientdel/<int:clientid>/')
def clientdel(clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    if current_user not in client.user and current_user.possition != "admin":
        abort(404)

    delClient(client)
    return redirect(url_for('client.clientlist'))






@client.route('/eventok/<int:eventid>/<int:clientid>')
def eventok(eventid, clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    if current_user not in client.user:
        abort(404)

    event = get_event(eventid)
    status = st_ok()
    change_status_event(client,event,status)
    return redirect(url_for('client.clientcart',clientid = clientid))



@client.route('/eventno/<int:eventid>/<int:clientid>')
def eventno(eventid, clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    if current_user not in client.user:
        abort(404)

    event = get_event(eventid)
    change_status_event(client,event, st_no())
    return redirect(url_for('client.clientcart',clientid = clientid))


@client.route('/eventproof/<int:eventid>/<int:clientid>')
def eventproof(eventid, clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    if current_user not in client.user:
        abort(404)
    event = get_event(eventid)
    status = st_proof()
    change_status_event(client,event,status)

    return redirect(url_for('client.clientcart',clientid = clientid))

@client.route('/eventnotready/<int:eventid>/<int:clientid>')
def eventnotready(eventid, clientid):
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    client = get_client(clientid)
    if current_user not in client.user:
        abort(404)

    event = get_event(eventid)
    status = st_notready()
    change_status_event(client,event,status)

    return redirect(url_for('client.clientcart',clientid = clientid))