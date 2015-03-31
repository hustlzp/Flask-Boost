# coding: utf-8
import os
import hashlib
import yaml
from flask import url_for
from jinja2 import Markup
from jsmin import jsmin
from cssmin import cssmin


class G(object):
    js_config = {}
    css_config = {}


def register_assets(app):
    static_path = app.static_folder
    G.js_config = yaml.load(open(os.path.join(static_path, 'js.yml'), 'r'))
    G.css_config = yaml.load(open(os.path.join(static_path, 'css.yml'), 'r'))

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


def build(app):
    print('Start building...')
    build_js(app)
    build_css(app)


def build_js(app):
    static_path = app.static_folder
    libs_path = G.js_config['libs']
    layout = G.js_config['layout']
    page_root_path = G.js_config['page']

    # libs.js
    libs_js_string = ""
    for lib_path in libs_path:
        with open(os.path.join(static_path, lib_path)) as js_file:
            libs_js_string += jsmin(js_file.read()).replace('\n', '').replace('\r', '')
    with open(os.path.join(static_path, 'build/libs.js'), "w") as text_file:
        text_file.write(libs_js_string)
    print('libs.js builded.')

    # page.js
    page_js_string = ""
    # layout
    for layout_path in layout:
        with open(os.path.join(static_path, layout_path)) as js_file:
            page_js_string += jsmin(js_file.read()).replace('\n', '').replace('\r', '')

    blueprints = app.blueprints.keys()

    page_js_prefix = "if(document.getElementsByTagName('body')[0].id === '%s'){(function(){"
    page_js_suffix = "})();}"

    page_root_path = os.path.join(static_path, page_root_path)
    for subdir in _get_immediate_subdirectories(page_root_path):
        if subdir in blueprints:
            subdir_path = os.path.join(page_root_path, subdir)
            for file in os.listdir(subdir_path):
                if file.endswith('.js'):
                    action = file[:-3]
                    page_id = "page-%s-%s" % (subdir, action)
                    with open(os.path.join(subdir_path, file)) as js_file:
                        page_js_string += page_js_prefix % page_id
                        page_js_string += jsmin(js_file.read()).replace('\n', '').replace('\r', '')
                        page_js_string += page_js_suffix
                        # print(file)

    with open(os.path.join(static_path, 'build/page.js'), "w") as text_file:
        text_file.write(page_js_string)
    print('page.js builded.')


def build_css(app):
    static_path = app.static_folder
    libs_path = G.css_config['libs']
    layout = G.css_config['layout']
    page_root_path = G.css_config['page']

    css_string = ""

    # libs
    for lib_path in libs_path:
        with open(os.path.join(static_path, lib_path)) as css_file:
            css_string += cssmin(css_file.read()).replace('\n', '').replace('\r', '')

    # layout
    for layout_path in layout:
        with open(os.path.join(static_path, layout_path)) as css_file:
            css_string += cssmin(css_file.read()).replace('\n', '').replace('\r', '')

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
                    with open(os.path.join(subdir_path, file)) as css_file:
                        css_string += page_css_prefix % page_id
                        css_string += cssmin(css_file.read()).replace('\n', '').replace('\r', '')
                        css_string += page_css_suffix
                        # print(file)

    with open(os.path.join(static_path, 'build/app.css'), "w") as text_file:
        text_file.write(css_string)
    print('app.css builded.')


def libs_js():
    """Generate js script tags for Flask app."""
    from flask import current_app

    script_paths = G.js_config['excluded_libs'][:]

    # if False:
    if current_app.debug:
        # 全局js引用
        script_paths += G.js_config['libs']
    else:
        script_paths.append('build/libs.js')
    return Markup(''.join([script(path) for path in script_paths]))


def page_js(template_reference):
    """Generate js script tags for Flask app."""
    from flask import current_app

    # if False:
    if current_app.debug:
        # layout
        script_paths = G.js_config['layout'][:]

        # page
        template_name = _get_template_name(template_reference)
        page_js_path = os.path.join(G.js_config['page'],
                                    template_name.replace('html', 'js'))
        script_paths.append(page_js_path)
        return Markup(''.join([script(path) for path in script_paths]))
    else:
        return Markup(script('build/page.js'))


def app_css(template_reference):
    """Generate js script tags for Flask app."""
    from flask import current_app

    css_paths = G.css_config['excluded_libs'][:]

    # if False:
    if current_app.debug:
        # libs + layout
        css_paths += G.css_config['libs'] + G.css_config['layout']
        # page
        template_name = _get_template_name(template_reference)
        page_css_path = os.path.join(G.css_config['page'],
                                     template_name.replace('html', 'css'))
        css_paths.append(page_css_path)
    else:
        css_paths.append('build/app.css')
    return Markup(''.join([link(path) for path in css_paths]))


def static(filename):
    """Generate static resource url.

    Hash asset content as query string, and cache it.
    """
    from flask import current_app

    if not hasattr(current_app, '_static_hash'):
        current_app._static_hash = {}

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
    template_name = _get_template_name(template_reference)
    return "page-%s" % template_name.replace('.html', '').replace('/', '-').replace('_', '-')


def _get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def _get_template_name(template_reference):
    """Get current template name."""
    return template_reference._TemplateReference__context.name
