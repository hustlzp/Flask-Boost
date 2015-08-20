# coding: utf-8
import functools
from flask import Response, json


def jsonify(func):
    """JSON decorator."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        if isinstance(r, tuple):
            code, data = r
        else:
            code, data = 200, r
        return Response(json.dumps(data), status=code, mimetype='application/json')

    return wrapper
