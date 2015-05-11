# coding: utf-8
from datetime import datetime
from ._base import db


class #{model|title}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<#{model|title} %s>' % self.name
