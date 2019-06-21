import re

from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField,SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired,ValidationError
from .model import User


class Registerform(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('用户名必须输入'),Length(min=3, max=12, message='用户名长度必须在3-12个字符')])
    password = PasswordField('密码',validators=[Length(6, 12, message='密码长度3-12位')])
    confirm = PasswordField('再次输入密码', validators=[DataRequired(), EqualTo('password', message='两次输入不一致')])
    email = StringField('邮箱', Email(message='格式不符'))

    def validate_username(self, field):
        res = User.query.filter(User.username == field.data).all()
        if res:
            raise ValidationError('用户名重复')

    def validate_password(self,field):
        if re.match(r'\d+$', field.data):
            raise ValidationError
