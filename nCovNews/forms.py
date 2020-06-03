from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField,TextAreaField,HiddenField
from wtforms.validators import DataRequired, Length, Email, Required ,NumberRange
from wtforms.validators import ValidationError
from nCovNews.datatype import USER

# 注册

def IDCheck_Register():
    def check(form, field):
        if len(field.data)!=9:
            raise ValidationError('请输入正确的9位学号')
        try:
            int(field.data)
        except:
            raise ValidationError('请输入正确的9位学号')
        if ( USER.query.filter_by(userid=field.data).first() ):
            raise ValidationError('此学号已注册')
    return check

def PasswordConfirmed():
    def check(form, field):
        if field.data!=form.password.data:
            raise ValidationError('密码不一致')
    return check

class RegisterForm(FlaskForm):
    id = StringField('学号', validators=[DataRequired(),IDCheck_Register()])
    name = StringField('昵称', validators=[DataRequired(),Length(min=1,max=9,message=u'昵称不超过9位')])
    password = PasswordField('密码', validators=[DataRequired(),Length(min=4,message=u'密码至少4位')])
    password2 = PasswordField('确认密码', validators=[DataRequired(),PasswordConfirmed()])
    register = SubmitField('注册')

# 登录

def IDCheck_Login():
    def check(form, field):
        if len(field.data)!=9:
            raise ValidationError('请输入正确的9位学号')
        try:
            int(field.data)
        except:
            raise ValidationError('请输入正确的9位学号')
        if ( USER.query.filter_by(userid=field.data).first() is None):
            raise ValidationError('该学号尚未注册')
    return check

def PasswordChcek():
    def check(form, field):
        user = USER.query.filter_by(userid=form.id.data).first()
        if user is None :
            raise ValidationError('')
        if field.data != user.password :
            raise ValidationError('密码错误')
    return check

class LoginForm(FlaskForm):
    id = StringField('学号', validators=[DataRequired(),IDCheck_Login()])
    password = PasswordField('密码', validators=[DataRequired(),PasswordChcek()])
    login = SubmitField('登录')

class PostForm(FlaskForm):
    word = TextAreaField('发表讨论',validators=[DataRequired()])
    post = SubmitField('发表')