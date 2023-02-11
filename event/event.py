from flask import Blueprint, url_for, render_template, redirect, request

from eventtype_helper import type_pay,type_report
from event_helper import get_event,get_all_event, delEvent,addEvent,editEvent
from controlorgan_helper import get_all_controlorgan, get_controlorgan
from vidotchet_helper import get_all_vidotchet, get_vidotchet
from tag_helper import get_all_tag
from opf_helper import get_all_opf
from nalog_helper import get_all_nalog

event = Blueprint('event', __name__, template_folder='templates')

@event.route('/')
def eventlist():
    events = get_all_event()
    return render_template('event/event_list.html', events = events)


@event.route('/<int:eventid>')
def eventcart(eventid):
    event = get_event(eventid)

    return render_template('event/event_cart.html', event = event)

# Добавление события
@event.route('/addevent', methods = ['GET', 'POST'])
def addevent():

    # формируем списки с параметрами
    tags = get_all_tag()
    controlorgans = get_all_controlorgan()
    vidotchets = get_all_vidotchet()
    opfs = get_all_opf()
    nalogs = get_all_nalog()
    eventtypes = [type_pay(),type_report()]



    # парсим форму
    event_name = request.form.get('name')
    data_start = request.form.get('data_start')
    data_end = request.form.get('data_end')
    controlorgan = get_controlorgan(request.form.get('controlorgan'))
    vidotchet = get_vidotchet(request.form.get('vidotchet'))
    shortname = request.form.get('shortname')
    type_event = request.form.get('type_event')


    eventTags = []
    for tag in tags:
        if (request.form.get(f'checktag_{tag.id}')) == 'on':
            eventTags.append(tag)

    eventOpfs = []
    for opf in opfs:
        if (request.form.get(f'checkopf_{opf.id}')) == 'on':
            eventOpfs.append(opf)

    eventNalogs = []
    for nalog in nalogs:
        if (request.form.get(f'checknalog_{nalog.id}')) == 'on':
            eventNalogs.append(nalog)


    # обрабатываем метод post
    if request.method == 'POST':

        try:
            addEvent(event_name,data_start,data_end,controlorgan,vidotchet,eventTags,eventNalogs,eventOpfs,type_event,shortname)
            return redirect(url_for('event.eventlist'))
        except:
            print('error')

    return render_template("event/add_event.html",
                           controlorgans = controlorgans,
                           vidotchets = vidotchets,
                           tags = tags,
                           opfs = opfs,
                           nalogs = nalogs,
                           eventtypes = eventtypes,
                           shotrname = shortname)

# Редактирование события
@event.route('/eventedit/<int:eventid>/', methods = ['GET', 'POST'])
def eventedit(eventid):

    event = get_event(eventid)

    # формируем списки с параметрами
    tags = get_all_tag()
    controlorgans = get_all_controlorgan()
    vidotchets = get_all_vidotchet()
    opfs = get_all_opf()
    nalogs = get_all_nalog()
    eventtypes = [type_pay(), type_report()]


    # парсим форму
    event_name = request.form.get('name')
    data_start = request.form.get('data_start')
    data_end = request.form.get('data_end')
    controlorgan = get_controlorgan(request.form.get('controlorgan'))
    vidotchet = get_vidotchet(request.form.get('vidotchet'))
    shortname = request.form.get('shortname')
    type_event = request.form.get('type_event')

    eventTags = []
    for tag in tags:
        if (request.form.get(f'checktag_{tag.id}')) == 'on':
            eventTags.append(tag)

    eventOpfs = []
    for opf in opfs:
        if (request.form.get(f'checkopf_{opf.id}')) == 'on':
            eventOpfs.append(opf)

    eventNalogs = []
    for nalog in nalogs:
        if (request.form.get(f'checknalog_{nalog.id}')) == 'on':
            eventNalogs.append(nalog)

    # обрабатываем метод post
    if request.method == 'POST':
        try:
            editEvent(event, event_name, data_start, data_end, controlorgan, vidotchet, eventTags, eventNalogs, eventOpfs, type_event,shortname)
            return redirect(url_for('event.eventlist'))
        except:
            print('error')


    return render_template("event/edit_event.html",
                           event = event,
                           controlorgans = controlorgans,
                           vidotchets = vidotchets,
                           tags = tags,
                           opfs = opfs,
                           nalogs = nalogs,
                           eventtypes = eventtypes,
                           shotrname = shortname)

# Удаление события
@event.route('/eventdel/<int:eventid>/')
def eventdel(eventid):
    event = get_event(eventid)
    delEvent(event)

    return redirect(url_for('event.eventlist'))