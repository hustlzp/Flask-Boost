# coding: utf-8
from flask import current_app, url_for


def absolute_url_for(endpoint, **values):
    """返回endpoint的绝对URL"""
    config = current_app.config
    site_domain = config.get('SITE_DOMAIN')
    relative_url = url_for(endpoint, **values)
    return join_url(site_domain, relative_url)


def join_url(pre_url, pro_url):
    return "%s/%s" % (pre_url.rstrip('/'), pro_url.lstrip('/'))
