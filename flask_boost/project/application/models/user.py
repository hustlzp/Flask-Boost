# coding: utf-8
import datetime
from ._base import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<User %s>' % self.name
