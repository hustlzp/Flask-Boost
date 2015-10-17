# coding: utf-8
from flask import render_template, Blueprint

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    """Index page."""
    return render_template('site/index/index.html')


@bp.route('/about')
def about():
    """About page."""
    return render_template('site/about/about.html')
