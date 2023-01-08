from flask import Blueprint
from flask import render_template, redirect, url_for
from models import db, Controlorgan
from .forms import ControlorganAdd,ControlorganEdit



controlorgan = Blueprint("contorolorgan", __name__, template_folder = 'templates')


# Вывод списка контролирующих органов на странице
@controlorgan.route('/')
def controlorganlist():
    controlorgans = Controlorgan.query.all()
    return render_template("controlorgan/controlorgan_list.html", controlorgans=controlorgans)


# Удаление тэга
@controlorgan.route('/controlorgandel/<int:controlorganid>/')
def controlorgandel(controlorganid):
    controlorgan = Controlorgan.query.get(controlorganid)
    db.session.delete(controlorgan)
    db.session.commit()

    return redirect(url_for('contorolorgan.controlorganlist'))



# Редактирование тэга
@controlorgan.route('/controlorganedit/<int:controlorganid>/', methods = ['GET', 'POST'])
def controlorganedit(controlorganid):

    controlorgan = Controlorgan.query.get(controlorganid)
    form = ControlorganEdit()
    val = controlorgan.control_name

    if form.validate_on_submit():
        controlorgan.control_name = form.controlorganname.data
        db.session.commit()
        return redirect(url_for('contorolorgan.controlorganlist'))

    return render_template("controlorgan/edit_controlorgan.html",controlorgan = controlorgan, form = form, value = val)

# Добавление тэга
@controlorgan.route('/addcontrolorgan', methods = ['GET', 'POST'])
def addcontrolorgan():
    form = ControlorganAdd()

    if form.validate_on_submit():
        name = form.controlorganname.data
        controlorgan = Controlorgan(name)
        db.session.add(controlorgan)
        db.session.commit()
        return redirect(url_for('contorolorgan.controlorganlist'))


    return render_template("controlorgan/add_controlorgan.html", form = form)