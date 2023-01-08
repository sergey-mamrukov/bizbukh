from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class TagAdd(FlaskForm):
    tagname = StringField('Название тэга', validators=[Length(min =2, max=80)])
    submit = SubmitField('Добавить')


class TagEdit(FlaskForm):
    tagname = StringField('Название тэга', validators=[Length(min =2, max=80)])
    submit = SubmitField('Изменить')