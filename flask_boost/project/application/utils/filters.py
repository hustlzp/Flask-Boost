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

    if value > now:
        return "right now"
    elif delta.days > 365:
        return '%d years ago' % (delta.days / 365)
    elif delta.days > 30:
        return '%d months ago' % (delta.days / 30)
    elif delta.days > 0:
        return '%d days ago' % delta.days
    elif delta.seconds > 3600:
        return '%d hours ago' % (delta.seconds / 3600)
    elif delta.seconds > 60:
        return '%d minutes ago' % (delta.seconds / 60)
    else:
        return 'right now'
