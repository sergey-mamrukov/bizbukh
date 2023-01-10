from flask import Blueprint, url_for, render_template, redirect, request
from models import db, Client, Opf, Tag, Systnalog

from db_helper import get_all_clients, get_client, get_eventredy_all, get_eventstatuses
from eventhelper import getEvents, getEventsbyobject, geteventok, addEventOk


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
    events = getEventsbyobject(client)
    tags = client.tag
    opfs = client.opf

    # status = get_eventstatuses()

    # addEventOk(client,events[0],status[0])
    geteventok()
    # geteventok()

    return render_template('client/client_cart.html', client=client, events=events, tags = tags, opfs=opfs)




@client.route('/clientedit/<int:clientid>', methods = ['GET', 'POST'])
def clientedit(clientid):
    client = get_client(clientid)
    tags = Tag.query.all()
    nalogs = Systnalog.query.all()
    opfs = Opf.query.all()






    if request.method == 'POST':

        # обнуление тэгов, опф и налога
        client.opf[:] = []
        client.tag[:] = []
        client.sysnalog[:] = []

        for tag in tags:
            if (request.form.get(f'checktag_{tag.id}')) == 'on':
                client.tag.append(tag)

        client.client_name = request.form.get('name')
        client.client_description = request.form.get('description')
        client.client_inn = request.form.get('inn')

        client.client_datazp = request.form.get('datazp')
        client.client_dataavansa = request.form.get('dataavans')


        client.opf.append(Opf.query.get(request.form.get('radioopf')))
        client.sysnalog.append(Systnalog.query.get(request.form.get('radionalog')))

        db.session.commit()


        return redirect(url_for('client.clientlist'))




    print(f"opf {client.opf}")
    print(f"sysnalog {client.sysnalog}")
    print(f"tag {client.tag}")




    return render_template("client/edit_client.html", tags = tags, nalogs=nalogs, opfs =opfs, client=client)



# Добавление организации
@client.route('/addclient', methods = ['GET', 'POST'])
def addclient():
    tags = Tag.query.all()
    nalogs = Systnalog.query.all()
    opfs = Opf.query.all()
    clnt = Client()


    if request.method == 'POST':

        print(f"nalog = {request.form.get('radionalog')}")

        for tag in tags:
            if (request.form.get(f'checktag_{tag.id}')) == 'on':
                clnt.tag.append(tag)

        clnt.client_name = request.form.get('name')
        clnt.client_description = request.form.get('description')
        clnt.client_inn = request.form.get('inn')

        clnt.client_datazp = request.form.get('datazp')
        clnt.client_dataavansa = request.form.get('dataavans')


        clnt.opf.append(Opf.query.get(request.form.get('radioopf')))
        clnt.sysnalog.append(Systnalog.query.get(request.form.get('radionalog')))



        db.session.add(clnt)
        db.session.commit()


        return redirect(url_for('client.clientlist'))


    return render_template("client/add_client.html", tags = tags, nalogs=nalogs, opfs =opfs)

# Удаление организации
@client.route('/clientdel/<int:clientid>/')
def clientdel(clientid):

    clnt = get_client(clientid)
    db.session.delete(clnt)
    db.session.commit()

    return redirect(url_for('client.clientlist'))

