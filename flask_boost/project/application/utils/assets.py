# coding: utf-8
import os
import hashlib
import yaml
import lesscpy
from functools import partial
from flask import url_for
from jinja2 import Markup
from jsmin import jsmin
from cssmin import cssmin
from six import StringIO
from .helpers import mkdir_p

# Config files
JS_CONFIG = "js.yml"
CSS_CONFIG = "css.yml"

# Output files
HEAD_JS = "build/libs.js"
BOTTOM_JS = "build/page.js"
HEAD_CSS = "build/app.css"


class G(object):
    """Global object."""
    js_config = {}
    css_config = {}
    debug = False


def register_assets(app):
    """Load assets config, and inject some helper funcions to jinja2 globals."""
    static_path = app.static_folder
    js_config_path = os.path.join(static_path, JS_CONFIG)
    css_config_path = os.path.join(static_path, CSS_CONFIG)

    G.debug = app.debug
    G.js_config = yaml.load(open(js_config_path, 'r'))
    G.css_config = yaml.load(open(css_config_path, 'r'))

    # Mkdir if output dir not exists
    output_dir = os.path.dirname(os.path.join(static_path, HEAD_JS))
    if not os.path.isdir(output_dir):
        mkdir_p(output_dir)

    # Reload app when js/css config file changes.
    if app.debug:
        app.run = partial(app.run, extra_files=[js_config_path, css_config_path])

    # Move excluded css libs to G.css_config['excluded_libs']
    G.css_config['excluded_libs'] = []
    for index, lib_path in enumerate(G.css_config['libs']):
        if lib_path.startswith('~'):
            lib_path = lib_path[1:]
            G.css_config['libs'][index] = lib_path
            G.css_config['excluded_libs'].append(lib_path)
    G.css_config['libs'] = [item for item in G.css_config['libs'] if
                            item not in G.css_config['excluded_libs']]

    # Move excluded js libs to G.js_config['excluded_libs']
    G.js_config['excluded_libs'] = []
    for index, lib_path in enumerate(G.js_config['libs']):
        if lib_path.startswith('~'):
            lib_path = lib_path[1:]
            G.js_config['libs'][index] = lib_path
            G.js_config['excluded_libs'].append(lib_path)
    G.js_config['libs'] = [item for item in G.js_config['libs'] if
                           item not in G.js_config['excluded_libs']]

    if not hasattr(app, '_static_hash'):
        app._static_hash = {}

    app.jinja_env.globals.update({
        'static': static,
        'libs_js': libs_js,
        'page_js': page_js,
        'app_css': app_css,
        'page_id': page_id
    })


def build(app):
    """Build assets."""
    print('Start building...')
    build_js(app)
    build_css(app)


def build_js(app):
    """Build js files.

    Include libs.js and page.js.
    """
    static_path = app.static_folder
    libs_path = G.js_config['libs']
    layout = G.js_config['layout']
    page_root_path = G.js_config['page']

    # Build libs.js
    libs_js_string = ""
    for lib_path in libs_path:
        with open(os.path.join(static_path, lib_path)) as js_file:
            libs_js_string += jsmin(js_file.read())

    libs_js_string = libs_js_string.replace('\n', '').replace('\r', '')
    with open(os.path.join(static_path, HEAD_JS), "w") as text_file:
        text_file.write(libs_js_string)
    print('libs.js builded.')

    # Build page.js
    page_js_string = ""

    # layout
    layout_js_prefix = "(function(){"
    layout_js_suffix = "})();"
    for layout_path in layout:
        with open(os.path.join(static_path, layout_path)) as js_file:
            page_js_string += layout_js_prefix + js_file.read() + layout_js_suffix

    # page
    blueprints = app.blueprints.keys()
    page_js_prefix = "if(document.documentElement.id==='%s'){(function(){"
    page_js_suffix = "})();}"

    page_root_path = os.path.join(static_path, page_root_path)
    for subdir in _get_immediate_subdirectories(page_root_path):
        if subdir in blueprints:
            subdir_path = os.path.join(page_root_path, subdir)
            for _file in os.listdir(subdir_path):
                if _file.endswith('.js'):
                    action = _file[:-3]
                    page_id = "page-%s-%s" % (subdir, action)
                    with open(os.path.join(subdir_path, _file)) as js_file:
                        page_js_string += page_js_prefix % page_id
                        page_js_string += js_file.read()
                        page_js_string += page_js_suffix
                        # print(file)

    page_js_string = jsmin(page_js_string).replace('\n', '').replace('\r', '')
    with open(os.path.join(static_path, BOTTOM_JS), "w") as text_file:
        text_file.write(page_js_string)
    print('page.js builded.')


def build_css(app):
    """Build css files.

    Include app.css.
    """
    from os.path import dirname

    static_path = app.static_folder
    libs = G.css_config['libs']
    layout = G.css_config['layout']
    page_root_path = G.css_config['page']

    app_css_string = ""

    # Build app.css

    # libs
    for lib in libs:
        lib_path = os.path.join(static_path, lib)

        with open(lib_path) as css_file:
            file_content = css_file.read()
            # Rewrite relative path to absolute path
            parent_dir = dirname(dirname(lib_path))
            absolute_path = "/static%s/" % parent_dir.split(static_path)[1]
            file_content = file_content.replace('../', absolute_path)
            app_css_string += cssmin(file_content)

    # layout
    for layout_path in layout:
        with open(os.path.join(static_path, layout_path)) as css_file:
            app_css_string += cssmin(css_file.read())

    # page
    blueprints = app.blueprints.keys()
    page_css_prefix = "#%s{"
    page_css_suffix = "}"

    page_root_path = os.path.join(static_path, page_root_path)
    for subdir in _get_immediate_subdirectories(page_root_path):
        if subdir in blueprints:
            subdir_path = os.path.join(page_root_path, subdir)
            for file in os.listdir(subdir_path):
                if file.endswith('.css'):
                    action = file[:-4]
                    page_id = "page-%s-%s" % (subdir, action)
                    file_path = os.path.join(subdir_path, file)
                    with open(file_path) as css_file:
                        page_css_string = page_css_prefix % page_id
                        page_css_string += css_file.read()
                        page_css_string += page_css_suffix
                        page_css_string = lesscpy.compile(StringIO(page_css_string), minify=True)
                        app_css_string += page_css_string
                        # print(file)

    app_css_string = app_css_string.replace('\n', '').replace('\r', '')
    with open(os.path.join(static_path, HEAD_CSS), "w") as text_file:
        text_file.write(app_css_string)
    print('app.css builded.')


def libs_js():
    """Generate js script tags for Flask app."""
    script_paths = G.js_config['excluded_libs'][:]

    # if False:
    if G.debug:
        # 全局js引用
        script_paths += G.js_config['libs']
    else:
        script_paths.append(HEAD_JS)
    return Markup(''.join([script(path) for path in script_paths]))


def page_js(template_reference):
    """Generate js script tags for Flask app."""

    # if False:
    if G.debug:
        # layout
        script_paths = G.js_config['layout'][:]

        # page
        template_name = _get_template_name(template_reference)
        page_js_path = os.path.join(G.js_config['page'],
                                    template_name.replace('html', 'js'))
        script_paths.append(page_js_path)
        return Markup(''.join([script(path) for path in script_paths]))
    else:
        return Markup(script(BOTTOM_JS))


def app_css(template_reference):
    """Generate js script tags for Flask app."""
    css_paths = G.css_config['excluded_libs'][:]

    # if False:
    if G.debug:
        # libs + layout
        css_paths += G.css_config['libs'] + G.css_config['layout']
        # page
        template_name = _get_template_name(template_reference)
        page_css_path = os.path.join(G.css_config['page'],
                                     template_name.replace('html', 'css'))
        css_paths.append(page_css_path)
    else:
        css_paths.append(HEAD_CSS)
    return Markup(''.join([link(path) for path in css_paths]))


def static(filename):
    """Generate static resource url.

    Hash asset content as query string, and cache it.
    """
    from flask import current_app

    url = url_for('static', filename=filename)

    if filename in current_app._static_hash:
        return current_app._static_hash[filename]

    path = os.path.join(current_app.static_folder, filename)
    if not os.path.exists(path):
        return None

    with open(path, 'r') as f:
        content = f.read()
        hash = hashlib.md5(content).hexdigest()

    url = '%s?v=%s' % (url, hash[:10])
    current_app._static_hash[filename] = url
    return url


def script(path):
    """Generate script tag."""
    script_path = static(path)
    if script_path:
        return Markup("<script type='text/javascript' src='%s'></script>" % script_path)
    else:
        return Markup("<!-- 404: %s -->" % path)


def link(path):
    """Generate link tag."""
    link_path = static(path)
    if link_path:
        return Markup("<link rel='stylesheet' href='%s'>" % link_path)
    else:
        return Markup("<!-- 404: %s -->" % path)


def page_id(template_reference):
    """Generate page with format: page-<controller>-<action>."""
    template_name = _get_template_name(template_reference)
    return "page-%s" % template_name.replace('.html', '').replace('/', '-').replace('_', '-')


def _get_immediate_subdirectories(_dir):
    """Get immediate subdirectories of a dir."""
    return [name for name in os.listdir(_dir)
            if os.path.isdir(os.path.join(_dir, name))]


def _get_template_name(template_reference):
    """Get current template name."""
    return template_reference._TemplateReference__context.name
