from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectMultipleField,SelectField
from wtforms.validators import Length, DataRequired

# Формы для работы с событиями
class EventAdd(FlaskForm):
    eventname = StringField('Название события', validators=[DataRequired()])
    eventdate = DateField('Дата события')
    eventnalog = SelectMultipleField('Система налогообложения',coerce=int)
    eventtag = SelectMultipleField('Тэги', coerce=int)
    eventopf = SelectMultipleField('Огранизационно-правовая форма',coerce=int)
    eventcontrolorgan = SelectField('Контролирующий орган', coerce=int)
    eventvidotchet = SelectField('Вид отчетности',coerce=int)


    submit = SubmitField('Добавить')


class EventEdit(FlaskForm):
    eventname = StringField('Название события', validators=[Length(min =2, max=80)])
    eventdate = DateField('Дата события')
    submit = SubmitField('Изменить')