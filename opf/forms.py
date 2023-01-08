from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

# Формы для работы с организационно-правовой формой
class OfpAdd(FlaskForm):
    opfname = StringField('Название организационно-правовой формы', validators=[Length(min =2, max=80)])
    submit = SubmitField('Добавить')


class OpfEdit(FlaskForm):
    opfname = StringField('Название организационно-правовой формы', validators=[Length(min =2, max=80)])
    submit = SubmitField('Изменить')