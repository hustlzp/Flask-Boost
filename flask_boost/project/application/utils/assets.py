# coding: utf-8
import os
import re
import glob2
import hashlib
import yaml
import lesscpy
from functools import partial
from flask import url_for
from jinja2 import Markup
from cssmin import cssmin
from six import StringIO
from .helpers import mkdir_p

# Config files
JS_CONFIG = "js.yml"
CSS_CONFIG = "css.yml"

# Output files
LIBS_JS = "build/libs.js"
APP_JS = "build/app.js"
LIBS_CSS = "build/libs.css"
APP_CSS = "build/app.css"


class G(object):
    """Global object."""
    js_config = {}
    css_config = {}
    debug = False
    static_path = ""


def register_assets(app):
    """Load assets config, and inject some helper funcions to jinja2 globals."""
    G.static_path = static_path = app.static_folder
    js_config_path = os.path.join(static_path, JS_CONFIG)
    css_config_path = os.path.join(static_path, CSS_CONFIG)

    G.debug = app.debug
    G.js_config = yaml.load(open(js_config_path, 'r'))
    G.css_config = yaml.load(open(css_config_path, 'r'))

    # Mkdir if output dir not exists
    output_dir = os.path.dirname(os.path.join(static_path, LIBS_JS))
    if not os.path.isdir(output_dir):
        mkdir_p(output_dir)

    # Reload app when js/css config file changes.
    if app.debug:
        app.run = partial(app.run, extra_files=[js_config_path, css_config_path])

    # Move excluded css libs to G.css_config['excluded_libs']
    G.css_config['excluded_libs'] = []
    for index, lib_path in enumerate(G.css_config['libs']):
        if lib_path.startswith(('~', 'http')):
            if lib_path.startswith('~'):
                lib_path = lib_path[1:]
            G.css_config['libs'][index] = lib_path
            G.css_config['excluded_libs'].append(lib_path)
    G.css_config['libs'] = [item for item in G.css_config['libs'] if
                            item not in G.css_config['excluded_libs']]

    # Move excluded js libs to G.js_config['excluded_libs']
    G.js_config['excluded_libs'] = []
    for index, lib_path in enumerate(G.js_config['libs']):
        if lib_path.startswith(('~', 'http')):
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
        'app_js': app_js,
        'libs_css': libs_css,
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

    Include libs.js and app.js.
    """
    static_path = app.static_folder
    libs = G.js_config['libs']
    layout = G.js_config['layout']
    page_root_path = G.js_config['page']

    # Build libs.js
    libs_js_string = ""
    for lib in libs:
        lib_path = os.path.join(static_path, lib)
        with open(lib_path) as js_file:
            libs_js_string += js_file.read() + "\r\n"

    lib_js_output_path = os.path.join(static_path, LIBS_JS)
    with open(lib_js_output_path, "w") as text_file:
        text_file.write(libs_js_string)

    os.system("uglifyjs %s -o %s -c warnings=false -m" % (lib_js_output_path, lib_js_output_path))
    print('libs.js builded.')

    # Build app.js
    app_js_string = ""

    # layout
    layout_js_prefix = "(function(){"
    layout_js_suffix = "})();"
    for layout_path in layout:
        with open(os.path.join(static_path, layout_path)) as js_file:
            app_js_string += layout_js_prefix + js_file.read() + layout_js_suffix

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
                    action = _file[:-3].replace('_', '-')
                    page_id = "page-%s-%s" % (subdir, action)
                    with open(os.path.join(subdir_path, _file)) as js_file:
                        app_js_string += page_js_prefix % page_id
                        app_js_string += js_file.read()
                        app_js_string += page_js_suffix

    app_js_output_path = os.path.join(static_path, APP_JS)
    with open(app_js_output_path, "w") as text_file:
        text_file.write(app_js_string)
    os.system("uglifyjs %s -o %s -c warnings=false -m" % (app_js_output_path, app_js_output_path))
    print('app.js builded.')


def build_css(app):
    """Build css files.

    Include libs.css and app.css.
    """
    static_path = app.static_folder
    libs = G.css_config['libs']
    layout = G.css_config['layout']
    page_root_path = G.css_config['page']

    # Build libs.css
    libs_css_string = ""
    for lib in libs:
        lib_path = os.path.join(static_path, lib)

        with open(lib_path) as css_file:
            file_content = css_file.read()
            # Rewrite relative path to absolute path
            file_content = _rewrite_relative_url(file_content, lib_path, static_path)
            libs_css_string += file_content

    libs_css_string = libs_css_string.replace('\n', '').replace('\r', '')
    with open(os.path.join(static_path, LIBS_CSS), "w") as text_file:
        text_file.write(libs_css_string)
    print('libs.css builded.')

    # Build app.css
    app_css_string = ""

    # layout
    for relative_layout_path in layout:
        absolute_layout_path = os.path.join(static_path, relative_layout_path)
        # 支持通配符
        if '*' in absolute_layout_path:
            for path in glob2.iglob(absolute_layout_path):
                with open(path) as css_file:
                    app_css_string += cssmin(css_file.read())
        else:
            with open(absolute_layout_path) as css_file:
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
                    action = file[:-4].replace('_', '-')
                    page_id = "page-%s-%s" % (subdir, action)
                    file_path = os.path.join(subdir_path, file)
                    with open(file_path) as css_file:
                        page_css_string = page_css_prefix % page_id
                        page_css_string += css_file.read()
                        page_css_string += page_css_suffix
                        page_css_string = lesscpy.compile(StringIO(page_css_string), minify=True)
                        app_css_string += page_css_string

    app_css_string = app_css_string.replace('\n', '').replace('\r', '')
    with open(os.path.join(static_path, APP_CSS), "w") as text_file:
        text_file.write(app_css_string)
    print('app.css builded.')


def libs_js():
    """Generate libs js script tags for Flask app."""
    script_tags = ""

    # Excluded libs
    for ex_lib in G.js_config['excluded_libs']:
        if ex_lib.startswith('http'):
            script_tags += script(ex_lib, absolute=True)
        else:
            script_tags += script(ex_lib)

    # if False:
    if G.debug:
        script_tags += ''.join(map(script, G.js_config['libs']))
    else:
        script_tags += script(LIBS_JS)
    return Markup(script_tags)


def app_js(template_reference):
    """Generate app js script tags for Flask app."""

    # if False:
    if G.debug:
        # layout
        script_paths = G.js_config['layout'][:]

        # page
        template_name = _get_template_name(template_reference)
        page_js_path = os.path.join(G.js_config['page'],
                                    template_name.replace('html', 'js'))
        script_paths.append(page_js_path)
        return Markup(''.join(map(script, script_paths)))
    else:
        return Markup(script(APP_JS))


def libs_css():
    """Generate libs css link tags for Flask app."""
    link_tags = ""

    # Excluded css libs
    for ex_lib in G.css_config['excluded_libs']:
        if ex_lib.startswith('http'):
            link_tags += link(ex_lib, absolute=True)
        else:
            link_tags += link(ex_lib)

    # if False:
    if G.debug:
        # libs
        link_tags += ''.join(map(link, G.css_config['libs']))
    else:
        link_tags += link(LIBS_CSS)
    return Markup(link_tags)


def app_css(template_reference):
    """Generate app css link tags for Flask app."""
    link_tags = ""

    # if False:
    if G.debug:
        # layout
        for layout_path in G.css_config['layout']:
            # 支持通配符
            if '*' in layout_path:
                for path in glob2.iglob(os.path.join(G.static_path, layout_path)):
                    relative_path = path.split(G.static_path)[1][1:]
                    link_tags += link(relative_path)
            else:
                link_tags += link(layout_path)

        # page
        template_name = _get_template_name(template_reference)
        page_css_path = os.path.join(G.css_config['page'],
                                     template_name.replace('html', 'css'))
        link_tags += link(page_css_path)
    else:
        link_tags += link(APP_CSS)
    return Markup(link_tags)


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


def script(path, absolute=False):
    """Generate script tag."""
    if absolute:
        return "<script type='text/javascript' src='%s'></script>" % path
    else:
        script_path = static(path)
        if script_path:
            return "<script type='text/javascript' src='%s'></script>" % script_path
        else:
            return "<!-- 404: %s -->" % path


def link(path, absolute=False):
    """Generate link tag."""
    if absolute:
        return "<link rel='stylesheet' href='%s'>" % path
    else:
        link_path = static(path)
        if link_path:
            return "<link rel='stylesheet' href='%s'>" % link_path
        else:
            return "<!-- 404: %s -->" % path


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


def _rewrite_relative_url(content, asset_path, static_path):
    """Rewrite relative url in `url('')` of css file to absolute url."""
    from os.path import dirname

    content = cssmin(content)
    pattern = re.compile(r"url\([\'\"]?([^\'\"/][^\'\"\)]+)[\'\"]?\)")

    for match in pattern.finditer(content):
        full = match.group(0)
        inner_url = match.group(1)

        if inner_url.startswith("data:"):
            continue

        if inner_url.startswith("../"):
            dir_path = dirname(dirname(asset_path))
            absolute_path = "%s/%s" % (dir_path, inner_url[3:])
        else:
            dir_path = dirname(asset_path)
            absolute_path = "%s/%s" % (dir_path, inner_url)

        absolute_url = "/static%s" % absolute_path.split(static_path)[1]
        result = "url('%s')" % absolute_url
        content = content.replace(full, result)
    return content
