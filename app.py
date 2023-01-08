from flask import Flask, render_template, url_for, redirect
from flask_migrate import Migrate

# Импорт моделей, форм
from models import db, Client, Opf, Systnalog
from client.forms import ClientAdd
from models import Tag


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


app = Flask(__name__)
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


# Точка входа
if __name__ == '__main__':
    app.run()