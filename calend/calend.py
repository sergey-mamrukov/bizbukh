from flask import Blueprint, render_template


calend = Blueprint('calend', __name__, template_folder='templates')


@calend.route('/')
def calendarwiev():
    return render_template('calendar/calendar.html')

@calend.route('/chart')
def chartview():
    return render_template('calendar/chart.html')