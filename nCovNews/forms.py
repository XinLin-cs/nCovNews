from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField,HiddenField
from wtforms.validators import DataRequired, Length, Email, Required

class LoginForm(FlaskForm):
    id = StringField('学号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    login = SubmitField('登陆')