# coding: utf-8
import datetime


def timesince(value):
    """Friendly time gap"""
    if not value:
        return ""

    if not isinstance(value, datetime.date):
        return value

    now = datetime.datetime.now()
    delta = now - value
    if delta.days > 365:
        return '%d年前' % (delta.days / 365)
    if delta.days > 30:
        return '%d个月前' % (delta.days / 30)
    if delta.days > 0:
        return '%d天前' % delta.days
    if delta.seconds > 3600:
        return '%d小时前' % (delta.seconds / 3600)
    if delta.seconds > 60:
        return '%d分钟前' % (delta.seconds / 60)
    return '刚刚'
