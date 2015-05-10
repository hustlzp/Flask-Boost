#!/usr/bin/env python
# coding: utf-8

"""
Flask Boost

Usage:
  boost new <project>
  boost generate controller <controller>
  boost generate form <form>
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


def new_project(args):
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
    logger.info(controller_file_path)

    # template dir
    template_dir_path = os.path.join(current_path, 'application/templates/%s' % controller_name)
    _mkdir_p(template_dir_path)
    logger.info(template_dir_path + "/")

    # css dir
    css_dir_path = os.path.join(current_path, 'application/static/css/%s' % controller_name)
    _mkdir_p(css_dir_path)
    logger.info(css_dir_path + "/")

    # js dir
    js_dir_path = os.path.join(current_path, 'application/static/js/%s' % controller_name)
    _mkdir_p(js_dir_path)
    logger.info(js_dir_path + "/")

    # form file
    _generate_form(controller_name)

    logger.info('Finish generating controller.')


def generate_form(args):
    """Generate form."""
    form_name = args.get('<form>')
    logger.info('Start generating form.')
    _generate_form(form_name)
    logger.info('Finish generating form.')


def main():
    args = docopt(__doc__, version="Flask-Boost {0}".format(__version__))
    if args.get('new'):
        new_project(args)
    elif args.get('generate') and args.get('controller'):
        generate_controller(args)
    elif args.get('generate') and args.get('form'):
        generate_form(args)


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
    new_file = open(abs_path, 'w')
    old_file = open(src_file)
    for line in old_file:
        new_line = line.replace('#{project}', project_name). \
            replace('#{project|title}', project_name.title())
        new_file.write(new_line)

    # Close file
    new_file.close()
    os.close(fh)
    old_file.close()

    # Move to new file
    shutil.move(abs_path, dst_file)


def _generate_form(form_name):
    form_template = os.path.join(dirname(abspath(__file__)), 'templates/form.py')
    current_path = os.getcwd()

    if not form_name:
        logger.warning('Form name cannot be empty.')
        return

    form_file_path = os.path.join(current_path, 'application/forms', form_name + '.py')
    shutil.copy(form_template, form_file_path)
    logger.info(form_file_path)


if __name__ == "__main__":
    main()
