from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------- Таблицы для связи многие ко многим для клиента -----------------
# Вспомогательная таблица тэги + клиент
tags = db.Table('tags', db.Column('tag_id', db.Integer, db.ForeignKey("tag.id")),
                  db.Column('client_id', db.Integer, db.ForeignKey("client.id")))



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

# Модель контролирующего органа
class Controlorgan(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    control_name = db.Column(db.String(80),unique=True)

    def __init__(self, controlname):
        self.control_name = controlname

# Модель вида отчетности
class Vidotchet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vid_name = db.Column(db.String(80),unique=True)

    def __init__(self, vidname):
        self.vid_name = vidname



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
    client_inn = db.Column(db.String(25))
    client_datazp = db.Column(db.Integer)
    client_dataavansa = db.Column(db.Integer)



    nalog_id = db.Column(db.Integer, db.ForeignKey('systnalog.id'))
    nalog = db.relationship('Systnalog', backref=db.backref("systnalog"))


    opf_id = db.Column(db.Integer, db.ForeignKey('opf.id'))
    opf = db.relationship('Opf', backref=db.backref("opf"))

    tag = db.relationship('Tag', secondary=tags,
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


    vidotchet_id = db.Column(db.Integer, db.ForeignKey('vidotchet.id'))
    vidotchet = db.relationship('Vidotchet', backref=db.backref("vidotchet"))

    controlorgan_id = db.Column(db.Integer, db.ForeignKey('controlorgan.id'))
    controlorgan = db.relationship('Controlorgan', backref=db.backref("controlorgan"))








