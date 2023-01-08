from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


nalogs = db.Table('nalogs', db.Column('nalog_id', db.Integer, db.ForeignKey("systnalog.id")),
                  db.Column('client_id', db.Integer, db.ForeignKey("client.id")))


opfs = db.Table('opfs', db.Column('opf_id', db.Integer, db.ForeignKey("opf.id")),
                  db.Column('client_id', db.Integer, db.ForeignKey("client.id")))


tags = db.Table('tags', db.Column('tag_id', db.Integer, db.ForeignKey("tag.id")),
                  db.Column('client_id', db.Integer, db.ForeignKey("client.id")))

eopfs = db.Table('eopfs', db.Column('opf_id', db.Integer, db.ForeignKey("opf.id")),
                    db.Column('event_id',db.Integer, db.ForeignKey('event.id')))

etags = db.Table('etags', db.Column('tag_id', db.Integer, db.ForeignKey("tag.id")),
                    db.Column('event_id',db.Integer, db.ForeignKey('event.id')))

enalogs = db.Table('enalogs', db.Column('sysnalog_id', db.Integer, db.ForeignKey("systnalog.id")),
                    db.Column('event_id',db.Integer, db.ForeignKey('event.id')))


econtrolorgan = db.Table('econtrolorgan', db.Column('controlorgan_id', db.Integer, db.ForeignKey("controlorgan.id")),
                    db.Column('event_id',db.Integer, db.ForeignKey('event.id')))

evidotchet = db.Table('evidotchet', db.Column('vidotchet_id', db.Integer, db.ForeignKey("vidotchet.id")),
                    db.Column('event_id',db.Integer, db.ForeignKey('event.id')))


# Модель организации
class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    client_name = db.Column(db.String(80),unique=True)
    client_description = db.Column(db.Text)
    client_inn = db.Column(db.String(15), unique=True)
    client_datazp = db.Column(db.Integer)
    client_dataavansa = db.Column(db.Integer)


    sysnalog = db.relationship('Systnalog', secondary = nalogs,
                               backref = db.backref('clients', lazy = 'dynamic'))


    opf = db.relationship('Opf', secondary=opfs,
                               backref=db.backref('clients', lazy='dynamic'))

    tag = db.relationship('Tag', secondary=tags,
                               backref=db.backref('clients', lazy='dynamic'))


    # def __init__(self, clientname):
    #     self.client_name = clientname


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

# Модель события
class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event_name = db.Column(db.String(80),unique=True)
    event_data_start = db.Column(db.Date())
    event_data_end = db.Column(db.Date())


    opf = db.relationship('Opf',secondary=eopfs,
                                    backref=db.backref('events', lazy='dynamic'))

    tag = db.relationship('Tag', secondary=etags,
                          backref=db.backref('events', lazy='dynamic'))

    nalog = db.relationship('Systnalog', secondary=enalogs,
                          backref=db.backref('events', lazy='dynamic'))


    contrologran = db.relationship('Controlorgan', secondary=econtrolorgan,
                          backref=db.backref('events', lazy='dynamic'))

    vidotchet = db.relationship('Vidotchet', secondary=evidotchet,
                                backref=db.backref('events', lazy='dynamic'))

    def __init__(self, eventname):
        self.event_name = eventname