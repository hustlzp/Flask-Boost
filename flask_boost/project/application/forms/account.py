# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from ..models import User


class SigninForm(Form):
    """Form for signin"""
    email = StringField('邮箱',
                        validators=[
                            DataRequired('邮箱不能为空'),
                            Email('邮箱格式错误')
                        ],
                        description='Email')

    password = PasswordField('密码',
                             validators=[DataRequired('密码不能为空')],
                             description='Password')

    def validate_email(self, field):
        user = User.query.filter(User.email == self.email.data).first()
        if not user:
            raise ValueError("账户不存在")

    def validate_password(self, field):
        if self.email.data:
            user = User.query.filter(User.email == self.email.data,
                                     User.password == self.password.data).first()
            if not user:
                raise ValueError('密码错误')
            else:
                self.user = user
