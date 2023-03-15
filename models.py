from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager



db = SQLAlchemy()
login_manager = LoginManager()


# ----------------- Таблицы для связи многие ко многим для клиента -----------------
# Вспомогательная таблица тэги + клиент
tags = db.Table('tags', db.Column('tag_id', db.Integer, db.ForeignKey("tag.id")),
                  db.Column('client_id', db.Integer, db.ForeignKey("client.id")))

users = db.Table('users', db.Column('user_id', db.Integer, db.ForeignKey("user.id")),
                    db.Column('client_id',db.Integer, db.ForeignKey('client.id')))

# ----------------- Таблицы для связи многие ко многим для события -----------------

# Вспомогательная таблица события + орг. форма
eopfs = db.Table('eopfs', db.Column('opf_id', db.Integer, db.ForeignKey("opf.id")),
                    db.Column('event_id',db.Integer, db.ForeignKey('event.id')))
# Вспомогательная таблица события + тэги
etags = db.Table('etags', db.Column('tag_id', db.Integer, db.ForeignKey("tag.id")),
                    db.Column('event_id',db.Integer, db.ForeignKey('event.id')))
# Вспомогательная таблица события + налог
enalogs = db.Table('enalogs', db.Column('sysnalog_id', db.Integer, db.ForeignKey("systnalog.id")),
                    db.Column('event_id',db.Integer, db.ForeignKey('event.id')))




# ----------------- Вспомогательные модели -----------------


# Модель тэга
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tag_name = db.Column(db.String(80), unique=True)

    def __init__(self, tagname):
        self.tag_name = tagname

# Модель организационно-правовой формы
class Opf(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    opf_name = db.Column(db.String(80),unique=True)

    def __init__(self, opfname):
        self.opf_name = opfname

# Модель системы налогообожения
class Systnalog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nalog_name = db.Column(db.String(80),unique=True)

    def __init__(self, nalogname):
        self.nalog_name = nalogname


# Модель выполненных событий
class Eventready(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref=db.backref("client"))

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship('Event', backref=db.backref("event"))

    status = db.Column(db.String())




# ----------------- Основные модели -----------------

# Модель организации
class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    client_name = db.Column(db.String(80))
    client_description = db.Column(db.Text)

    # Реквизиты организации
    client_inn = db.Column(db.String(25))
    client_fullname = db.Column(db.Text())
    client_shortname = db.Column(db.Text())
    client_uraddress = db.Column(db.Text())
    client_pochtaddress = db.Column(db.Text())
    client_kpp = db.Column(db.Text())
    client_ogrn = db.Column(db.Text())
    client_director = db.Column(db.Text())
    client_osnovanie = db.Column(db.Text())

    # Банковские реквизиты
    client_bank_name = db.Column(db.Text())
    client_bank_bik = db.Column(db.Text())
    client_bank_rs = db.Column(db.Text())
    client_bank_ks = db.Column(db.Text())

    # Контакты организации
    client_contact_name = db.Column(db.Text())
    client_contact_phone = db.Column(db.Text())
    client_contact_email = db.Column(db.Text())


    nalog_id = db.Column(db.Integer, db.ForeignKey('systnalog.id'))
    nalog = db.relationship('Systnalog', backref=db.backref("systnalog"))


    opf_id = db.Column(db.Integer, db.ForeignKey('opf.id'))
    opf = db.relationship('Opf', backref=db.backref("opf"))

    tag = db.relationship('Tag', secondary=tags,
                               backref=db.backref('clients', lazy='dynamic'))

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', cascade="all,delete", backref=db.backref("cl-company"))

    user = db.relationship('User', secondary= users,cascade="all,delete",
                          backref=db.backref('clients', lazy='dynamic'))






# Модель события
class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event_name = db.Column(db.Text())
    event_data_start = db.Column(db.Date())
    event_data_end = db.Column(db.Date())

    type_event = db.Column(db.String)
    short_name = db.Column(db.String)


    opf = db.relationship('Opf',secondary=eopfs,
                                    backref=db.backref('events', lazy='dynamic'))

    tag = db.relationship('Tag', secondary=etags,
                          backref=db.backref('events', lazy='dynamic'))

    nalog = db.relationship('Systnalog', secondary=enalogs,
                          backref=db.backref('events', lazy='dynamic'))




# Модель персонального события
class PersonalEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.Text())
    short_name = db.Column(db.Text())
    event_data_end = db.Column(db.Date())
    status = db.Column(db.Text())
    is_zp = db.Column(db.Boolean())
    type_event = db.Column(db.String)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref=db.backref("pe-client"))



# Модель компании (бухфирмы)
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.Text())

    count_user = db.Column(db.Integer())
    count_client = db.Column(db.Integer())
    company_status = db.Column(db.Text())
    company_date_created = db.Column(db.Date())




@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)


# # Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String())
    password = db.Column(db.String())
    possition = db.Column(db.String())

    name = db.Column(db.String())
    surname = db.Column(db.String())


    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    # company = db.relationship('Company', cascade="all,delete", backref=db.backref("us-company"))
    company = db.relationship('Company', backref=db.backref("us-company"))








