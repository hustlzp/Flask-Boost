# coding: utf-8
from flask import Blueprint, render_template

bp = Blueprint('#{controller}', __name__)


@bp.route('/#{controller}/action')
def action():
    return render_template('#{controller}/action.html')
