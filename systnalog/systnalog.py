from flask import Blueprint, render_template,redirect, url_for
from models import db, Systnalog
from .forms import NalogAdd,NalogEdit

systnalog = Blueprint('systnalog', __name__, template_folder='templates')


# Вывод списка систем налогообложения на странице
@systnalog.route('/')
def naloglist():
    systnalog = Systnalog.query.all()
    return render_template("nalog/nalog_list.html",systnalogs = systnalog)

# Удаление системы налогообложения
@systnalog.route('/nalogdel/<int:nalogid>/')
def nalogdel(nalogid):

    systnalog = Systnalog.query.get(nalogid)
    db.session.delete(systnalog)
    db.session.commit()

    return redirect(url_for('systnalog.naloglist'))


# Редактирование системы налогообложения
@systnalog.route('/nalogedit/<int:nalogid>/', methods = ['GET', 'POST'])
def nalogedit(nalogid):


    systnalog = Systnalog.query.get(nalogid)
    form = NalogEdit()
    val = systnalog.nalog_name

    if form.validate_on_submit():


        systnalog.nalog_name = form.nalogname.data
        db.session.commit()
        return redirect(url_for('systnalog.naloglist'))

    return render_template("nalog/edit_nalog.html",systnalog = systnalog, form = form, value = val)

# Добавление системы налогообложения
@systnalog.route('/addnalog', methods = ['GET', 'POST'])
def addnalog():
    form = NalogAdd()

    if form.validate_on_submit():
        name = form.nalogname.data
        systnalog = Systnalog(name)
        db.session.add(systnalog)
        db.session.commit()
        return redirect(url_for('systnalog.naloglist'))


    return render_template("nalog/add_nalog.html", form = form)