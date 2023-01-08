from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


# Формы для работы с системой налогообложения
class NalogAdd(FlaskForm):
    nalogname = StringField('Название системы налогообложения', validators=[Length(min =2, max=80)])
    submit = SubmitField('Добавить')


class NalogEdit(FlaskForm):
    nalogname = StringField('Название системы налогообложения', validators=[Length(min =2, max=80)])
    submit = SubmitField('Изменить')