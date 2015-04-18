# coding: utf-8
import os
import errno
from flask import current_app, url_for


def absolute_url_for(endpoint, **values):
    """Absolute url for endpoint."""
    config = current_app.config
    site_domain = config.get('SITE_DOMAIN')
    relative_url = url_for(endpoint, **values)
    return join_url(site_domain, relative_url)


def join_url(pre_url, pro_url):
    return "%s/%s" % (pre_url.rstrip('/'), pro_url.lstrip('/'))


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
