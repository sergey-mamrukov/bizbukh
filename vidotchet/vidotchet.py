from flask import Blueprint
from flask import render_template, redirect, url_for
from models import db, Vidotchet
from .forms import VidotchetAdd,VidotchetEdit



vidotchet = Blueprint("vidotchet", __name__, template_folder = 'templates')


# Вывод списка контролирующих органов на странице
@vidotchet.route('/')
def vidotchetlist():
    vidotchets = Vidotchet.query.all()
    return render_template("vidotchet/vidotchet_list.html", vidotchets=vidotchets)


# Удаление тэга
@vidotchet.route('/vidotchetdel/<int:vidotchetid>/')
def vidotchetdel(vidotchetid):
    vidotchet = Vidotchet.query.get(vidotchetid)
    db.session.delete(vidotchet)
    db.session.commit()

    return redirect(url_for('vidotchet.vidotchetlist'))



# Редактирование тэга
@vidotchet.route('/vidotchetedit/<int:vidotchetid>/', methods = ['GET', 'POST'])
def vidotchetedit(vidotchetid):

    vidotchet = Vidotchet.query.get(vidotchetid)
    form = VidotchetEdit()
    val = vidotchet.vid_name

    if form.validate_on_submit():
        vidotchet.vid_name = form.vidotchetname.data
        db.session.commit()
        return redirect(url_for('vidotchet.vidotchetlist'))

    return render_template("vidotchet/edit_vidotchet.html",vidotchet = vidotchet, form = form, value = val)

# Добавление тэга
@vidotchet.route('/addvidotchet', methods = ['GET', 'POST'])
def addvidotchet():
    form = VidotchetAdd()

    if form.validate_on_submit():
        name = form.vidotchetname.data
        vidotchet = Vidotchet(name)
        db.session.add(vidotchet)
        db.session.commit()
        return redirect(url_for('vidotchet.vidotchetlist'))


    return render_template("vidotchet/add_vidotchet.html", form = form)