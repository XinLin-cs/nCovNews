from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField,HiddenField
from wtforms.validators import DataRequired, Length, Email, Required

class NameForm(FlaskForm):
    name = StringField('昵称', validators=[Required()])
    login = SubmitField('登陆')
    register = SubmitField('注册')