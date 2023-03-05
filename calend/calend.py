from flask import Blueprint, render_template,request
import datetime
from event_helper import get_event,get_events_on_day


calend = Blueprint('calend', __name__, template_folder='templates')


@calend.route('/')
def calendarwiev():
    return render_template('calendar/calendar.html')


@calend.route('/chart')
def chartview():
    return render_template('calendar/chart.html')

@calend.route('/change/<int:eventid>')
def eventview(eventid):
    event = get_event(eventid)
    return render_template('calendar/event-clients-edit.html', event = event)

@calend.route('/events', methods = ['POST', 'GET'])
def caleventlist():
    date = datetime.date.today()
    events = get_events_on_day(str(date))

    if request.method == "POST":
        print("post")
        events = get_events_on_day(request.form.get("date"))
        date = request.form.get("date")
        return render_template('calendar/list.html', events=events, date=date)

    # print (date)


    return render_template('calendar/list.html',events=events, date=date)