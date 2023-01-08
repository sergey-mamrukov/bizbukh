from flask import Blueprint, render_template,redirect, url_for
from models import db, Opf
from .forms import OfpAdd, OpfEdit


opf = Blueprint('opf', __name__,template_folder='templates')

# Вывод списка ОПФ на странице
@opf.route('/')
def opflist():
    opf = Opf.query.all()
    return render_template("opf/opf_list.html",opfs = opf)

# Удаление ОПФ
@opf.route('/opfdel/<int:opfid>/')
def opfdel(opfid):

    opf = Opf.query.get(opfid)
    db.session.delete(opf)
    db.session.commit()

    return redirect(url_for('opf.opflist'))


# Редактирование ОПФ
@opf.route('/opfedit/<int:opfid>/', methods = ['GET', 'POST'])
def opfedit(opfid):


    opf = Opf.query.get(opfid)
    form = OpfEdit()
    val = opf.opf_name

    if form.validate_on_submit():


        opf.opf_name = form.opfname.data
        db.session.commit()
        return redirect(url_for('opf.opflist'))

    return render_template("opf/edit_opf.html",opf = opf, form = form, value = val)

# Добавление ОПФ
@opf.route('/addopf', methods = ['GET', 'POST'])
def addopf():
    form = OfpAdd()

    if form.validate_on_submit():
        name = form.opfname.data
        opf = Opf(name)
        db.session.add(opf)
        db.session.commit()
        return redirect(url_for('opf.opflist'))


    return render_template("opf/add_opf.html", form = form)
