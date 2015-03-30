# coding: utf-8
import os
import hashlib
import yaml
from flask import url_for
from jinja2 import Markup
from jsmin import jsmin


class G(object):
    js_config = {}
    css_config = {}


def register_assets(app):
    static_path = app.static_folder
    G.js_config = yaml.load(open(os.path.join(static_path, 'js.yml'), 'r'))
    G.css_config = {}
    # Register jinja functions
    app.jinja_env.globals['libs_js'] = libs_js


def build(app):
    static_path = app.static_folder
    js_config = yaml.load(open(os.path.join(static_path, 'js.yml'), 'r'))
    libs_path = js_config['libs']
    layout = js_config['layout']
    page_root_path = js_config['page']

    # libs.js
    libs_js_string = ""
    for lib_path in libs_path:
        with open(os.path.join(static_path, lib_path)) as js_file:
            libs_js_string += jsmin(js_file.read()).replace('\n', '').replace('\r', '')
    with open(os.path.join(static_path, 'build/libs.js'), "w") as text_file:
        text_file.write(libs_js_string)

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
    for subdir in get_immediate_subdirectories(page_root_path):
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
                    print(file)

    with open(os.path.join(static_path, 'build/page.js'), "w") as text_file:
        text_file.write(page_js_string)


def libs_js():
    from flask import current_app

    """Generate js script tags for Flask app."""
    # if False:
    if current_app.debug:
        # 全局js引用
        scripts = [script(path) for path in G.js_config['libs']]
        return Markup(''.join(scripts))
    else:
        return Markup(script('build/libs.js'))


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
    return "<script type='text/javascript' src='%s'></script>" % static(path)


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
