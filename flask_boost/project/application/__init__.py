# coding: utf-8
import sys
import os

# Insert project root path to sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

import time
import logging
from flask import Flask, request, url_for, g, render_template
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.contrib.fixers import ProxyFix
from six import iteritems
from .utils.account import get_current_user
from config import load_config

# convert python's encoding to utf8
try:
    from imp import reload

    reload(sys)
    sys.setdefaultencoding('utf8')
except (AttributeError, NameError):
    pass


def create_app():
    """Create Flask app."""
    config = load_config()

    app = Flask(__name__)
    app.config.from_object(config)

    if not hasattr(app, 'production'):
        app.production = not app.debug and not app.testing

    # Proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # CSRF protect
    CsrfProtect(app)

    if app.debug or app.testing:
        DebugToolbarExtension(app)

        # Serve static files
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/pages': os.path.join(app.config.get('PROJECT_PATH'), 'application/pages')
        })
    else:
        # Log errors to stderr in production mode
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.ERROR)

        # Enable Sentry
        if app.config.get('SENTRY_DSN'):
            from .utils.sentry import sentry

            sentry.init_app(app, dsn=app.config.get('SENTRY_DSN'))

        # Serve static files
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': os.path.join(app.config.get('PROJECT_PATH'), 'output/static'),
            '/pkg': os.path.join(app.config.get('PROJECT_PATH'), 'output/pkg'),
            '/pages': os.path.join(app.config.get('PROJECT_PATH'), 'output/pages')
        })

    # Register components
    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    register_hooks(app)

    return app


def register_jinja(app):
    """Register jinja filters, vars, functions."""
    import jinja2
    from .utils import filters, permissions, helpers

    if app.debug or app.testing:
        my_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader([
                os.path.join(app.config.get('PROJECT_PATH'), 'application/macros'),
                os.path.join(app.config.get('PROJECT_PATH'), 'application/pages')
            ])
        ])
    else:
        my_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader([
                os.path.join(app.config.get('PROJECT_PATH'), 'output/macros'),
                os.path.join(app.config.get('PROJECT_PATH'), 'output/pages')
            ])
        ])
    app.jinja_loader = my_loader

    app.jinja_env.filters.update({
        'timesince': filters.timesince
    })

    def url_for_other_page(page):
        """Generate url for pagination."""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        combined_args = dict(view_args.items() + args.items())
        combined_args['page'] = page
        return url_for(request.endpoint, **combined_args)

    rules = {}
    for endpoint, _rules in iteritems(app.url_map._rules_by_endpoint):
        if any(item in endpoint for item in ['_debug_toolbar', 'debugtoolbar', 'static']):
            continue
        rules[endpoint] = [{'rule': rule.rule} for rule in _rules]

    app.jinja_env.globals.update({
        'absolute_url_for': helpers.absolute_url_for,
        'url_for_other_page': url_for_other_page,
        'rules': rules,
        'permissions': permissions
    })


def register_db(app):
    """Register models."""
    from .models import db

    db.init_app(app)


def register_routes(app):
    """Register routes."""
    from . import controllers
    from flask.blueprints import Blueprint

    for module in _import_submodules_from_package(controllers):
        bp = getattr(module, 'bp')
        if bp and isinstance(bp, Blueprint):
            app.register_blueprint(bp)


def register_error_handle(app):
    """Register HTTP error pages."""

    @app.errorhandler(403)
    def page_403(error):
        return render_template('site/403/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('site/404/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('site/500/500.html'), 500


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


def _import_submodules_from_package(package):
    import pkgutil

    modules = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__,
                                                         prefix=package.__name__ + "."):
        modules.append(__import__(modname, fromlist="dummy"))
    return modules
