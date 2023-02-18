import json

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate


from eventready_helper import change_status
from eventstatus_helper import st_no,st_ok,st_notready,st_proof
from event_helper import get_event
from client_helper import get_all_clients,get_client
from ajax import get_client_info, get_client_info_on_date,get_event_info,get_zp_info
from client_events import get_client_event_all,get_event_clients_all,get_status_event
from personalevent_helper import get_personal_event, changestatusPersonalEvent,delPersonalEvent, addPersonalEvent


# Импорт моделей, форм
from models import db


# Импорт конфигурации
from config import Config


# Импорт Blueprints
from tag.tag import tag
from opf.opf import opf
from systnalog.systnalog import systnalog
from client.client import client
from event.event import event
from calend.calend import calend




app = Flask(__name__)
cors = CORS(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(tag, url_prefix='/tag')
app.register_blueprint(opf, url_prefix='/opf')
app.register_blueprint(systnalog, url_prefix='/systnalog')
app.register_blueprint(client,url_prefix='/client')
app.register_blueprint(event, url_prefix='/event')
app.register_blueprint(calend, url_prefix='/calendar')


# Главный роут
@app.route('/')
def index():
    return render_template("index.html")

# AJAX роуты

# возвращает информацию по клиентам с событиями
@app.route('/ajax/get')
@cross_origin()
def ajax1():

    if request.args:
        client_id = request.args.get('clientid')
        date = request.args.get('date')
        if client_id and date:
            client = get_client(client_id)
            info = get_client_info_on_date(client, date)


            return jsonify(info)

    else:
        allclients = get_all_clients()
        resp = []
        for client in allclients:
            info = get_client_info(client)
            resp.append(info)

        return jsonify(resp)


# возвращает все события
@app.route('/ajax/getallevents')
@cross_origin()
def ajax2():

    events = []
    info = []

    clients = get_all_clients()
    for client in clients:
        events.extend(get_client_event_all(client))
        if client.client_datazp != 0:
            info.append(get_zp_info("Зарплата полное название","Зарплата", client.client_datazp))

        if client.client_dataavansa != 0:

            info.append(get_zp_info("Аванс полное название","Аванс", client.client_dataavansa))

    resevents = list(set(events))


    for event in resevents:
        info.append(get_event_info(event))



    return jsonify(info)

# меняет статус события
@app.route('/ajax/changestatus/<int:clientid>/<int:eventid>/<int:status>')
@cross_origin()
def ajax3(clientid, eventid, status):
    client = get_client(clientid)
    event = get_event(eventid)

    # 1 - st_ok
    # 2 - st_no
    # 3 - st_proof
    # 4 - st_notready

    if status == 1:
        change_status(client,event,st_ok())
        return jsonify({"newstatus": st_ok()})
    if status == 2:
        change_status(client,event,st_no())
        return jsonify({"newstatus": st_no()})

    if status == 3:
        change_status(client,event,st_proof())
        return jsonify({"newstatus": st_proof()})

    if status == 4:
        change_status(client,event,st_notready())
        return jsonify({"newstatus": st_notready()})

    return jsonify("error")

# возвращает всех клиентов у события
@app.route('/ajax/getallclientsforevent/<int:eventid>')
@cross_origin()
def ajax4(eventid):


    event = get_event(eventid)
    clients = get_event_clients_all(event)

    result = []

    for client in clients:
        result.append({"clientname":client.client_name,
                       "clientid": client.id,
                       "status" :get_status_event(client,event)})


    return jsonify(result)

# меняет статус персонального события
@app.route('/ajax/changestatuspersonal/<int:clientid>/<int:eventid>/<int:status>')
@cross_origin()
def ajax5(clientid, eventid, status):
    client = get_client(clientid)
    pevent = get_personal_event(eventid)

    # 1 - st_ok
    # 2 - st_no
    # 3 - st_proof
    # 4 - st_notready

    if status == 1:
        changestatusPersonalEvent(pevent,st_ok())
        return jsonify({"newstatus": st_ok()})
    if status == 2:
        changestatusPersonalEvent(pevent,st_no())
        return jsonify({"newstatus": st_no()})

    if status == 3:
        changestatusPersonalEvent(pevent,st_proof())
        return jsonify({"newstatus": st_proof()})

    if status == 4:
        changestatusPersonalEvent(pevent,st_notready())
        return jsonify({"newstatus": st_notready()})

    return jsonify("error")

# удаление персонального события
@app.route('/ajax/delpersonalevent/<int:clientid>/<int:eventid>/<int:status>')
@cross_origin()
def ajax6(clientid, eventid, status):

    pevent = get_personal_event(eventid)
    delPersonalEvent(pevent)

    return jsonify("error")

# удаление персонального события
@app.route('/ajax/addpevent/', methods = ['POST'])
@cross_origin()
def ajax7():
    info = json.loads(str(request.data, encoding='utf-8'))
    client = get_client(int(info['clientid']))
    nameevent = info['eventname']
    date = info['date']

    print(f"clientid = {info['clientid']} date = {info['date']}")

    addPersonalEvent(client,nameevent,date)



    return jsonify("error")




# Точка входа
if __name__ == '__main__':
    app.run(host='0.0.0.0')