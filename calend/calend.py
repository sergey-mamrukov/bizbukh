from flask import Blueprint, render_template


calend = Blueprint('calend', __name__, template_folder='templates')


@calend.route('/')
def calendarwiew():
    return render_template('calendar/calendarajax.html')