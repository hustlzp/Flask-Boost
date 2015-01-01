# coding: utf-8
from flask import session, abort, flash, redirect, url_for
from permission import Role
from ..models import User


class VisitorRole(Role):
    def check(self):
        return 'user_id' not in session

    def deny(self):
        return redirect(url_for('site.index'))


class UserRole(Role):
    def check(self):
        return 'user_id' in session

    def deny(self):
        flash('Sign in first.')
        return redirect(url_for('account.signin'))


class AdminRole(Role):
    def base(self):
        return UserRole()

    def check(self):
        user_id = int(session['user_id'])
        user = User.query.filter(User.id == user_id).first()
        return user and user.is_admin

    def deny(self):
        abort(403)
