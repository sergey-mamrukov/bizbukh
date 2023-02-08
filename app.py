import json

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate

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
from controlorgan.controlorgan import controlorgan
from vidotchet.vidotchet import vidotchet

from eventready_helper import change_status
from eventstatus_helper import st_no,st_ok,st_notready,st_proof
from event_helper import get_event
from client_helper import get_all_clients,get_client
from ajax import get_client_info, get_client_info_on_date


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
app.register_blueprint(controlorgan, url_prefix='/controlorgan')
app.register_blueprint(vidotchet, url_prefix='/vidotchet')

# Главный роут
@app.route('/')
def index():
    return render_template("index.html")


# AJSX роуты
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



@app.route('/ajax/changestatus',methods = ["POST"])
@cross_origin()
def ajax2():
    data = request.get_data()

    print(data)
    return jsonify("error")



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







# Точка входа
if __name__ == '__main__':
    app.run(host='0.0.0.0')