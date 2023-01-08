from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class VidotchetAdd(FlaskForm):
    vidotchetname = StringField('Название вида отчетности', validators=[Length(min =2, max=80)])
    submit = SubmitField('Добавить')


class VidotchetEdit(FlaskForm):
    vidotchetname = StringField('Название вида отчетности', validators=[Length(min =2, max=80)])
    submit = SubmitField('Изменить')