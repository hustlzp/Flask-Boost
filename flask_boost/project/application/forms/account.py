# coding: utf-8
from flask_wtf import Form
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
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
            user = User.query.filter(User.email == self.email.data).first()
            if not user or not user.check_password(self.password.data):
                raise ValueError('密码错误')
            else:
                self.user = user


class SignupForm(Form):
    """Form for signin"""
    name = StringField('用户名',
                       validators=[DataRequired('用户名不能为空')],
                       description='用户名')

    email = StringField('邮箱',
                        validators=[
                            DataRequired(message="邮箱不能为空"),
                            Email(message="无效的邮箱")
                        ],
                        description='邮箱')

    password = PasswordField('密码',
                             validators=[DataRequired('密码不能为空')],
                             description='密码')

    repassword = PasswordField('重复密码',
                               validators=[
                                   DataRequired('重复密码不能为空'),
                                   EqualTo('password', message='两次输入密码不一致')
                               ],
                               description='重复密码')

    def validate_name(self, field):
        user = User.query.filter(User.name == self.name.data).first()
        if user:
            raise ValueError('用户名已存在')

    def validate_email(self, field):
        user = User.query.filter(User.email == self.email.data).first()
        if user:
            raise ValueError('邮箱已被注册')