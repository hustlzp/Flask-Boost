# coding: utf-8
from flask import session
from ..models import User


def signin_user(user, permenent=True):
    """Sign in user"""
    session.permanent = permenent
    session['user_id'] = user.id


def signout_user():
    """Sign out user"""
    session.pop('user_id', None)


def get_current_user():
    """获取当前user，同时进行session有效性的检测"""
    if not 'user_id' in session:
        return None
    user = User.query.filter(User.id == session['user_id']).first()
    if not user:
        signout_user()
        return None
    return user