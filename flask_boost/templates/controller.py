# coding: utf-8
from flask import Blueprint

bp = Blueprint('#{controller}', __name__)


@bp.route('/#{controller}/action')
def action():
    pass
