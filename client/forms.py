from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, widgets
from wtforms.validators import Length


# Формы для работы с организациями
class ClientAdd(FlaskForm):
    clientname = StringField('Название организации', validators=[Length(min =2, max=80)])
    systnalog = SelectField('Система налогообложения')

    opf = SelectField('Организационно-правовая форма')

    tags = SelectMultipleField('Тэги',
        widget=widgets.ListWidget(prefix_label=False, html_tag='ol'),
        option_widget=widgets.CheckboxInput())

    submit = SubmitField('Добавить')


class ClientEdit(FlaskForm):
    clientname = StringField('Название организации', validators=[Length(min =2, max=80)])
    submit = SubmitField('Изменить')