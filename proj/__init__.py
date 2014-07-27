# coding: utf-8
import sys
from flask import Flask, request, url_for, g, render_template, session
from flask_wtf.csrf import CsrfProtect
from flask.ext.uploads import configure_uploads
from flask_debugtoolbar import DebugToolbarExtension
from . import config
from .utils.account import get_current_user

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')


def create_app():
    """创建Flask app"""
    app = Flask(__name__)
    app.config.from_object(config)

    # CSRF protect
    CsrfProtect(app)

    if app.debug:
        DebugToolbarExtension(app)
    else:
        from .utils.sentry import sentry

        sentry.init_app(app)

    # from .mails import mail
    # mail.init_app(app)

    # 注册组件
    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    register_uploadsets(app)

    # before every request
    @app.before_request
    def before_request():
        g.user = get_current_user()

    return app


def register_jinja(app):
    """注册模板全局变量和全局函数"""
    from jinja2 import Markup
    from .utils import filters

    app.jinja_env.filters['timesince'] = filters.timesince

    # inject vars into template context
    @app.context_processor
    def inject_vars():
        return dict(
            g_var_name=0,
        )

    def url_for_other_page(page):
        """Generate url for pagination"""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        args['page'] = page
        view_args.update(args)
        return url_for(request.endpoint, **view_args)

    def static(filename):
        """生成静态资源url"""
        return url_for('static', filename=filename)

    def bower(filename):
        """生成bower资源url"""
        return static("bower_components/%s" % filename)

    def script(path):
        """生成script标签"""
        return Markup("<script type='text/javascript' src='%s'></script>" % static(path))

    def link(path):
        """生成link标签"""
        return Markup("<link rel='stylesheet' href='%s'></script>" % static(path))

    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    app.jinja_env.globals['static'] = static
    app.jinja_env.globals['bower'] = bower
    app.jinja_env.globals['script'] = script
    app.jinja_env.globals['link'] = link


def register_db(app):
    """注册Model"""
    from .models import db

    db.init_app(app)


def register_routes(app):
    """注册路由"""
    from .controllers import site

    app.register_blueprint(site.bp, url_prefix='')


def register_error_handle(app):
    """注册HTTP错误页面"""

    @app.errorhandler(403)
    def page_403(error):
        return render_template('site/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('site/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('site/500.html'), 500


def register_uploadsets(app):
    """注册UploadSets"""
    from .utils.uploadsets import avatars

    configure_uploads(app, (avatars))


app = create_app()