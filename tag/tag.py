from flask import Blueprint
from flask import render_template, redirect, url_for
from models import db, Tag
from .forms import TagAdd, TagEdit



tag = Blueprint("tag", __name__, template_folder = 'templates')


# Вывод списка тэгов на странице
@tag.route('/')
def taglist():
    tags = Tag.query.all()
    return render_template("tag/tag_list.html",tags = tags)


@tag.route('/<int:tagid>')
def tagcart(tagid):
    tag = Tag.query.get(tagid)


    return render_template("tag/tag_cart.html",tag = tag)



# Удаление тэга
@tag.route('/tagdel/<int:tagid>/')
def tagdel(tagid):
    tag = Tag.query.get(tagid)
    db.session.delete(tag)
    db.session.commit()

    return redirect(url_for('tag.taglist'))



# Редактирование тэга
@tag.route('/tagedit/<int:tagid>/', methods = ['GET', 'POST'])
def tagedit(tagid):

    tag = Tag.query.get(tagid)
    form = TagEdit()
    val = tag.tag_name

    if form.validate_on_submit():
        tag.tag_name = form.tagname.data
        db.session.commit()
        return redirect(url_for('taglist'))

    return render_template("tag/edit_tag.html",tag = tag, form = form, value = val)

# Добавление тэга
@tag.route('/addtag', methods = ['GET', 'POST'])
def addtag():
    form = TagAdd()

    if form.validate_on_submit():
        name = form.tagname.data
        tag = Tag(name)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('tag.taglist'))


    return render_template("tag/add_tag.html", form = form)