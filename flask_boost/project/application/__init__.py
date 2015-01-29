# coding: utf-8
import sys
import os

# Insert project root path to sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

import hashlib
import time
from flask import Flask, request, url_for, g, render_template
from flask_wtf.csrf import CsrfProtect
from flask.ext.uploads import configure_uploads
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.contrib.fixers import ProxyFix
from .utils.account import get_current_user
from config import load_config

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')


def create_app():
    """Create Flask app."""
    app = Flask(__name__)

    config = load_config()
    app.config.from_object(config)

    if not hasattr(app, 'production'):
        app.production = not app.debug and not app.testing

    # Proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # CSRF protect
    CsrfProtect(app)

    # Enable Sentry in production mode
    if app.production:
        from .utils.sentry import sentry

        sentry.init_app(app, dsn=app.config.get('SENTRY_DSN'))
    else:
        DebugToolbarExtension(app)

        # Serve static files during development
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/uploads': os.path.join(app.config.get('PROJECT_PATH'), 'uploads')
        })

    # Register components
    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    register_uploadsets(app)
    register_hooks(app)

    return app


def register_jinja(app):
    """Register jinja filters, vars, functions."""
    from jinja2 import Markup
    from .utils import filters

    if not hasattr(app, '_static_hash'):
        app._static_hash = {}

    app.jinja_env.filters['timesince'] = filters.timesince

    # Inject vars into template context
    @app.context_processor
    def inject_vars():
        from .utils import permissions

        return dict(
            permissions=permissions
        )

    def url_for_other_page(page):
        """Generate url for pagination."""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        combined_args = dict(view_args.items() + args.items())
        combined_args['page'] = page
        return url_for(request.endpoint, **combined_args)

    def static(filename):
        """Generate static resource url.

        Hash asset content as query string, and cache it.
        """
        url = url_for('static', filename=filename)

        if filename in app._static_hash:
            return app._static_hash[filename]

        path = os.path.join(app.static_folder, filename)
        if not os.path.exists(path):
            return url

        with open(path, 'r') as f:
            content = f.read()
            hash = hashlib.md5(content).hexdigest()

        url = '%s?v=%s' % (url, hash[:10])
        app._static_hash[filename] = url
        return url

    def script(path):
        """Generate script tag."""
        return Markup("<script type='text/javascript' src='%s'></script>" % static(path))

    def link(path):
        """Generate link tag."""
        return Markup("<link rel='stylesheet' href='%s'>" % static(path))

    def page_script(template_reference):
        """Generate script tag for current page."""
        template_name = _get_template_name(template_reference)
        return script('js/%s' % template_name.replace('html', 'js'))

    def page_link(template_reference):
        """Generate link tag for current page."""
        template_name = _get_template_name(template_reference)
        return link('css/%s' % template_name.replace('html', 'css'))

    def page_name(template_reference):
        template_name = _get_template_name(template_reference)
        return "page-%s" % template_name.replace('.html', '').replace('/', '-').replace('_', '-')

    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    app.jinja_env.globals['static'] = static
    app.jinja_env.globals['script'] = script
    app.jinja_env.globals['page_script'] = page_script
    app.jinja_env.globals['link'] = link
    app.jinja_env.globals['page_link'] = page_link
    app.jinja_env.globals['page_name'] = page_name


def register_db(app):
    """Register models."""
    from .models import db

    db.init_app(app)


def register_routes(app):
    """Register routes."""
    from .controllers import site, account

    app.register_blueprint(site.bp, url_prefix='')
    app.register_blueprint(account.bp, url_prefix='/account')


def register_error_handle(app):
    """Register HTTP error pages."""

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
    """Register UploadSets."""
    from .utils.uploadsets import avatars

    configure_uploads(app, (avatars))


def register_hooks(app):
    """Register hooks."""

    @app.before_request
    def before_request():
        g.user = get_current_user()
        if g.user and g.user.is_admin:
            g._before_request_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta * 1000
        return response


def _get_template_name(template_reference):
    """Get current template name."""
    return template_reference._TemplateReference__context.name
