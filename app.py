import json

from flask import Flask, render_template, jsonify, request, redirect,url_for
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_login import current_user, login_user, logout_user


from eventready_helper import change_status_event
from eventstatus_helper import st_no,st_ok,st_notready,st_proof
from event_helper import get_event
from client_helper import get_all_clients,get_client
from ajax import get_client_info, get_client_info_on_date,get_event_info,get_zp_info
from client_events import get_client_event_all,get_event_clients_all,get_status_event
from personalevent_helper import get_personal_event, changestatusPersonalEvent,delPersonalEvent, addPersonalEvent

from company_helper import addCompany, getCompany
from user_helper import addUser



# Импорт моделей, форм
from models import db, login_manager, User


# Импорт конфигурации
from config import Config


# Импорт Blueprints
from tag.tag import tag
from opf.opf import opf
from systnalog.systnalog import systnalog
from client.client import client
from event.event import event
from calend.calend import calend
from company.company import company
from user.user import user





app = Flask(__name__)
cors = CORS(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)


app.register_blueprint(tag, url_prefix='/tag')
app.register_blueprint(opf, url_prefix='/opf')
app.register_blueprint(systnalog, url_prefix='/systnalog')
app.register_blueprint(client, url_prefix='/client')
app.register_blueprint(event, url_prefix='/event')
app.register_blueprint(calend, url_prefix='/calendar')
app.register_blueprint(company, url_prefix='/company')
app.register_blueprint(user, url_prefix='/user')





# Главный роут
@app.route('/')
def index():
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    if current_user.possition == "user":
        company = current_user.company
        return render_template("user.html", company=company)

    if current_user.possition == "admin":
        company = current_user.company
        return render_template("admin.html", company=company)

    if current_user.possition == "super-admin":
        company = current_user.company
        return render_template("super-admin.html", company=company)


    return redirect(url_for("login"))



@app.route("/registration", methods = ['POST', 'GET'])
def registration():
    if request.method == 'POST':
        company_name = request.form.get("company_name")
        login = request.form.get("login")
        password = request.form.get("password")
        possition = 'admin'

        company = addCompany(company_name)

        addUser(login,password,company, possition)

        print(f"name = {company_name}, login = {login}, password = {password}")

        return redirect(url_for("login"))


    return render_template("registration.html")



@app.route("/login", methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == 'POST':
        login = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter(User.login == login).first()
        if user and user.password == password:
            login_user(user)
            return (redirect(url_for("index")))
        else: print ("error login or password")

        print(f"login = {login}, password = {password}")


    return render_template("authorization.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))





















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
        change_status_event(client,event,st_ok())
        return jsonify({"newstatus": st_ok()})
    if status == 2:
        change_status_event(client,event,st_no())
        return jsonify({"newstatus": st_no()})

    if status == 3:
        change_status_event(client,event,st_proof())
        return jsonify({"newstatus": st_proof()})

    if status == 4:
        change_status_event(client,event,st_notready())
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

def testr():
    pass



# Точка входа
if __name__ == '__main__':
    app.run(host='0.0.0.0')