#!/usr/bin/env python
# coding: utf-8

"""
Flask Boost

Usage:
  boost new <project>
  boost -v | --version
  boost -h | --help

Options:
  -h, --help          Help information.
  -v, --version       Show version.
"""

import os
import logging
from logging import StreamHandler, DEBUG
from os.path import dirname, abspath
from tempfile import mkstemp
from docopt import docopt
import shutil
import errno
from flask_boost import __version__

logger = logging.getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler())


def execute(args):
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

            _rewrite_and_copy(src_file, dst_file, project_name)

            if filename in ['development_sample.py', 'production_sample.py']:
                dst_file = os.path.join(dst_dir, "%s.py" % filename.split('_')[0])
                _rewrite_and_copy(src_file, dst_file, project_name)

    logger.info('Finish generating project files.')


def main():
    args = docopt(__doc__, version="Flask-Boost {0}".format(__version__))
    execute(args)


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


if __name__ == "__main__":
    main()
