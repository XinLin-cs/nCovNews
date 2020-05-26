from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField,TextAreaField,HiddenField
from wtforms.validators import DataRequired, Length, Email, Required ,NumberRange
from wtforms.validators import ValidationError
from nCovNews import db

class LoginForm(FlaskForm):
    id = StringField('学号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    login = SubmitField('登陆')

def IDCheck():
    def check(form, field):
        if len(field.data)!=9:
            raise ValidationError('请输入正确的9位学号')
        try:
            # int(field.data)
            pass
        except:
            raise ValidationError('请输入正确的9位学号')
    return check

def PasswordConfirmed():
    def check(form, field):
        if field.data!=form.password.data:
            raise ValidationError('密码不一致')
    return check

class RegisterForm(FlaskForm):
    id = StringField('学号', validators=[DataRequired(),IDCheck()])
    name = StringField('昵称', validators=[DataRequired(),Length(min=1,max=9,message=u'昵称不超过9位')])
    password = PasswordField('密码', validators=[DataRequired(),Length(min=4,message=u'密码至少4位')])
    password2 = PasswordField('确认密码', validators=[DataRequired(),PasswordConfirmed()])
    register = SubmitField('注册')