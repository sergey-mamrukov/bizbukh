from flask import Blueprint, url_for, render_template, redirect
from models import Event, db,Tag,Opf,Systnalog, Client,Vidotchet,Controlorgan
from.forms import EventAdd, EventEdit

event = Blueprint('event', __name__, template_folder='templates')

@event.route('/')
def eventlist():
    form = EventAdd()
    events = Event.query.all()
    return render_template('event/event_list.html', events = events, form = form)

@event.route('/<int:eventid>')
def eventcart(eventid):
    event = Event.query.get(eventid)
    alltag = []
    client = []
    cl = Client.query.all()

    for tag in event.tag:
        alltag.append(tag.tag_name)
        for cl in tag.clients:
            client.append(cl)



    for opf in event.opf:
        alltag.append(opf.opf_name)
        for cl in opf.clients:
            client.append(cl)

    for nalog in event.nalog:
        alltag.append(nalog.nalog_name)
        for cl in nalog.clients:
            client.append(cl)



    return render_template('event/event_cart.html', event = event, alltag = alltag, client =set(client))

# Удаление события
@event.route('/eventdel/<int:eventid>/')
def eventdel(eventid):

    event = Event.query.get(eventid)
    db.session.delete(event)
    db.session.commit()

    return redirect(url_for('event.eventlist'))


# Редактирование события
@event.route('/eventedit/<int:eventid>/', methods = ['GET', 'POST'])
def eventedit(eventid):


    event = Event.query.get(eventid)
    form = EventEdit()
    val = event.event_name

    if form.validate_on_submit():
        event.event_name = form.eventname.data
        db.session.commit()
        return redirect(url_for('event.eventlist'))

    return render_template("event/edit_event.html",event = event, form = form, value = val)

# Добавление события
@event.route('/addevent', methods = ['GET', 'POST'])
def addevent():
    form = EventAdd()
    tags = Tag.query.all()
    nalogs = Systnalog.query.all()
    opfs = Opf.query.all()
    controlorgans = Controlorgan.query.all()
    vidotchets = Vidotchet.query.all()


    ftags = []
    for tag in tags:
        ftags.append([tag.id,tag.tag_name])
    form.eventtag.choices = ftags

    fopfs = []
    for opf in opfs:
        fopfs.append([opf.id,opf.opf_name])
    form.eventopf.choices = fopfs

    fnalogs = []
    for nalog in nalogs:
        fnalogs.append([nalog.id,nalog.nalog_name])
    form.eventnalog.choices = fnalogs

    fcontrolorgans =[]
    for controlorgan in controlorgans:
        fcontrolorgans.append([controlorgan.id,controlorgan.control_name])
    form.eventcontrolorgan.choices = fcontrolorgans

    fvidotchets = []
    for vidotchet in vidotchets:
        fvidotchets.append([vidotchet.id,vidotchet.vid_name])
    form.eventvidotchet.choices = fvidotchets


    if form.validate_on_submit():
        name = form.eventname.data
        event = Event(name)


        event.event_data = form.eventdate.data

        for op in form.eventopf.data:
            event.opf.append(Opf.query.get(op))

        for sn in form.eventnalog.data:
            event.nalog.append(Systnalog.query.get(sn))

        for tg in form.eventtag.data:
            event.tag.append(Tag.query.get(tg))

        vo = form.eventvidotchet.data
        event.vidotchet.append(Vidotchet.query.get(vo))

        co = form.eventcontrolorgan.data
        event.contrologran.append(Controlorgan.query.get(co))


        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event.eventlist'))


    return render_template("event/add_event.html", form = form)
