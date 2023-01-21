from flask import Blueprint, render_template
from .calendarhelper import getmonthyname,getdaqyname


from event_helper import getCountEventsonDate
import calendar, datetime


from client_helper import get_all_clients


calend = Blueprint('calend', __name__, template_folder='templates')



@calend.route('/')
def calendarwiew():

    year = 2022
    month = 12

    c = calendar.Calendar()
    rez = c.itermonthdays2(year, month)

    result = list(rez)
    res = []
    date = []

    days = []

    for r in result:
        if r[0] == 0:
            continue
        res.append([r[0], getdaqyname(r[1])])
        date.append(f"{year}-{month}-{r[0]}")
        days.append(r[0])


    monthname = getmonthyname(month)

    cal = [monthname, res, year, date]

    clientid = 31
    clients = []


    allclients = get_all_clients()


    for client in allclients:
        dayevent = []
        for day in days:
            d = datetime.date(year,month,day)
            count = getCountEventsonDate(d,client.id)
            if count > 0:
                dayevent.append(count)
            else: dayevent.append(0)

        clients.append([client, dayevent])


    return render_template('calendar/calendar.html', cal = cal, clients = clients, year = year, month = month)