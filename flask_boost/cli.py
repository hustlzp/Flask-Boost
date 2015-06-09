#!/usr/bin/env python
# coding: utf-8

"""
Flask Boost

Usage:
  boost new <project>
  boost new controller <controller>
  boost new action <controller> <action> [-t]
  boost new form <form>
  boost new model <model>
  boost -v | --version
  boost -h | --help

Options:
  -h, --help          Help information.
  -v, --version       Show version.
"""

import sys
import os

# Insert project root path to sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

import logging
from logging import StreamHandler, DEBUG
from os.path import dirname, abspath
from tempfile import mkstemp
from docopt import docopt
import shutil
import errno
from flask_boost import __version__

# If you add #{project} in a file, add the file ext here
REWRITE_FILE_EXTS = ('.html', '.conf', '.py', '.json', '.md')

logger = logging.getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler())


def generate_project(args):
    """New project."""
    # Project templates path
    src = os.path.join(dirname(abspath(__file__)), 'project')

    project_name = args.get('<project>')

    if not project_name:
        logger.warning('Project name cannot be empty.')
        return

    # Destination project path
    dst = os.path.join(os.getcwd(), project_name)

    if os.path.isdir(dst):
        logger.warning('Project directory already exists.')
        return

    logger.info('Start generating project files.')

    _mkdir_p(dst)

    for src_dir, sub_dirs, filenames in os.walk(src):
        # Build and create destination directory path
        relative_path = src_dir.split(src)[1].lstrip('/')
        dst_dir = os.path.join(dst, relative_path)

        if src != src_dir:
            _mkdir_p(dst_dir)

        # Copy, rewrite and move project files
        for filename in filenames:
            if filename in ['development.py', 'production.py']:
                continue

            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)

            if filename.endswith(REWRITE_FILE_EXTS):
                _rewrite_and_copy(src_file, dst_file, project_name)
            else:
                shutil.copy(src_file, dst_file)

            if filename in ['development_sample.py', 'production_sample.py']:
                dst_file = os.path.join(dst_dir, "%s.py" % filename.split('_')[0])
                _rewrite_and_copy(src_file, dst_file, project_name)

    logger.info('Finish generating project files.')


def generate_controller(args):
    """Generate controller, include the controller file, template & css & js directories."""
    controller_template = os.path.join(dirname(abspath(__file__)), 'templates/controller.py')
    test_template = os.path.join(dirname(abspath(__file__)), 'templates/unittest.py')
    controller_name = args.get('<controller>')
    current_path = os.getcwd()

    logger.info('Start generating controller.')

    if not controller_name:
        logger.warning('Controller name cannot be empty.')
        return

    # controller file
    with open(controller_template, 'r') as template_file:
        controller_file_path = os.path.join(current_path, 'application/controllers',
                                            controller_name + '.py')
        with open(controller_file_path, 'w+') as controller_file:
            for line in template_file:
                new_line = line.replace('#{controller}', controller_name)
                controller_file.write(new_line)
    logger.info("New: %s" % controller_file_path)

    # test file
    with open(test_template, 'r') as template_file:
        test_file_path = os.path.join(current_path, 'tests',
                                      'test_%s.py' % controller_name)
        with open(test_file_path, 'w+') as test_file:
            for line in template_file:
                new_line = line.replace('#{controller}', controller_name) \
                    .replace('#{controller|title}', controller_name.title())
                test_file.write(new_line)
    logger.info("New: %s" % test_file_path)

    # template dir
    template_dir_path = os.path.join(current_path, 'application/templates/%s' % controller_name)
    _mkdir_p(template_dir_path)
    logger.info("New: %s" % template_dir_path + "/")

    # css dir
    css_dir_path = os.path.join(current_path, 'application/static/css/%s' % controller_name)
    _mkdir_p(css_dir_path)
    logger.info("New: %s/" % css_dir_path)

    # js dir
    js_dir_path = os.path.join(current_path, 'application/static/js/%s' % controller_name)
    _mkdir_p(js_dir_path)
    logger.info("New: %s/" % js_dir_path)

    # form file
    _generate_form(controller_name)

    logger.info('Finish generating controller.')


def generate_action(args):
    """Generate action."""
    controller = args.get('<controller>')
    action = args.get('<action>')
    with_template = args.get('-t')
    current_path = os.getcwd()

    controller_file_path = os.path.join(current_path, 'application/controllers', controller + '.py')
    if not os.path.exists(controller_file_path):
        logger.warning("The controller %s does't exist." % controller)
        return

    if with_template:
        action_source_path = os.path.join(dirname(abspath(__file__)), 'templates/action.py')
    else:
        action_source_path = os.path.join(dirname(abspath(__file__)), 'templates/action_without_template.py')
    action_html_template_path = os.path.join(dirname(abspath(__file__)), 'templates/action.html')

    # Add action source codes
    with open(action_source_path, 'r') as action_source_file:
        with open(controller_file_path, 'a') as controller_file:
            for action_line in action_source_file:
                new_line = action_line.replace('#{controller}', controller). \
                    replace('#{action}', action)
                controller_file.write(new_line)
    logger.info("Updated: %s" % controller_file_path)

    if with_template:
        controller_template_dir_path = os.path.join(current_path, 'application/templates/%s' % controller)
        if not os.path.exists(controller_template_dir_path):
            os.makedirs(controller_template_dir_path)

        # Create action html file
        action_html_file_path = os.path.join(controller_template_dir_path, '%s.html' % action)
        with open(action_html_template_path, 'r') as action_html_template_file:
            with open(action_html_file_path, 'w') as action_html_file:
                for line in action_html_template_file:
                    new_line = line.replace('#{action|title}', action.title())
                    action_html_file.write(new_line)
        logger.info("New: %s" % action_html_file_path)

        # Create action js file
        controller_js_dir_path = os.path.join(current_path, 'application/static/js/%s' % controller)
        if not os.path.exists(controller_js_dir_path):
            os.makedirs(controller_js_dir_path)
        action_js_file_path = os.path.join(controller_js_dir_path, '%s.js' % action)
        open(action_js_file_path, 'a').close()
        logger.info("New: %s" % action_js_file_path)

        # Create action less file
        controller_css_dir_path = os.path.join(current_path, 'application/static/css/%s' % controller)
        if not os.path.exists(controller_css_dir_path):
            os.makedirs(controller_css_dir_path)

        action_less_template_path = os.path.join(dirname(abspath(__file__)), 'templates/action.less')
        action_less_file_path = os.path.join(controller_css_dir_path, '%s.less' % action)
        shutil.copy(action_less_template_path, action_less_file_path)
        logger.info("New: %s" % action_less_file_path)


def generate_form(args):
    """Generate form."""
    form_name = args.get('<form>')
    logger.info('Start generating form.')
    _generate_form(form_name)
    logger.info('Finish generating form.')


def generate_model(args):
    """Generate model."""
    model_name = args.get('<model>')
    logger.info('Start generating model.')

    model_template = os.path.join(dirname(abspath(__file__)), 'templates/model.py')
    current_path = os.getcwd()

    if not model_name:
        logger.warning('Model name cannot be empty.')
        return

    with open(model_template, 'r') as template_file:
        model_file_path = os.path.join(current_path, 'application/models',
                                       model_name + '.py')
        with open(model_file_path, 'w+') as model_file:
            for line in template_file:
                new_line = line.replace('#{model|title}', model_name.title())
                model_file.write(new_line)
    logger.info("New: %s" % model_file_path)

    with open(os.path.join(current_path, 'application/models/__init__.py'), 'a') as package_file:
        package_file.write('\nfrom .%s import *' % model_name)

    logger.info('Finish generating model.')


def main():
    args = docopt(__doc__, version="Flask-Boost {0}".format(__version__))
    if args.get('new'):
        if args.get('controller'):
            generate_controller(args)
        elif args.get('form'):
            generate_form(args)
        elif args.get('model'):
            generate_model(args)
        elif args.get('action'):
            generate_action(args)
        else:
            generate_project(args)
    else:
        print(args)


def _mkdir_p(path):
    """mkdir -p path"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def _rewrite_and_copy(src_file, dst_file, project_name):
    """Replace vars and copy."""
    # Create temp file
    fh, abs_path = mkstemp()

    with open(abs_path, 'w') as new_file:
        with open(src_file, 'r') as old_file:
            for line in old_file:
                new_line = line.replace('#{project}', project_name). \
                    replace('#{project|title}', project_name.title())
                new_file.write(new_line)

    # Move to new file
    shutil.move(abs_path, dst_file)
    os.close(fh)


def _generate_form(form_name):
    form_template = os.path.join(dirname(abspath(__file__)), 'templates/form.py')
    current_path = os.getcwd()

    if not form_name:
        logger.warning('Form name cannot be empty.')
        return

    form_file_path = os.path.join(current_path, 'application/forms', form_name + '.py')
    shutil.copy(form_template, form_file_path)
    logger.info("New: %s" % form_file_path)

    with open(os.path.join(current_path, 'application/forms/__init__.py'), 'a') as package_file:
        package_file.write('\nfrom .%s import *' % form_name)


if __name__ == "__main__":
    main()
