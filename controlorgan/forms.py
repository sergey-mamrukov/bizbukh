from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class ControlorganAdd(FlaskForm):
    controlorganname = StringField('Название контролирующего органа', validators=[Length(min =2, max=80)])
    submit = SubmitField('Добавить')


class ControlorganEdit(FlaskForm):
    controlorganname = StringField('Название контролирующего органа', validators=[Length(min =2, max=80)])
    submit = SubmitField('Изменить')