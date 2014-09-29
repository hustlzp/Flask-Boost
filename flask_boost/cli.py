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
from os.path import dirname, abspath
from tempfile import mkstemp
from docopt import docopt
import shutil
import errno
from flask_boost import __version__

logger = logging.getLogger(__name__)


def mkdir_p(path):
    """mkdir -p path"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def execute(args):
    # 源路径
    src = os.path.join(dirname(abspath(__file__)), 'project')

    # 目的路径
    project_name = args['<project>']
    dst = os.path.join(os.getcwd(), project_name)

    logger.info('Start generating project files.')

    # 创建项目根文件夹
    mkdir_p(dst)

    for src_dir, sub_dirs, filenames in os.walk(src):
        # 构建目标文件夹路径
        relative_path = src_dir.split(src)[1].lstrip('/')
        dst_dir = os.path.join(dst, relative_path)

        # 创建目标文件夹
        if src != src_dir:
            # print(dirpath)
            # print(dst_path)
            mkdir_p(dst_dir)

        # 移动文件
        for filename in filenames:
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)
            shutil.copy(src_file, dst_file)

            # Create temp file
            fh, abs_path = mkstemp()
            new_file = open(abs_path, 'w')
            old_file = open(src_file)
            for line in old_file:
                new_file.write(line.replace('#{project}', project_name))

            # Close file
            new_file.close()
            os.close(fh)
            old_file.close()

            # Move to new file
            shutil.move(abs_path, dst_file)

    logger.info('Finish generating project files.')


def main():
    args = docopt(__doc__, version="Flask-Boost {0}".format(__version__))
    execute(args)


if __name__ == "__main__":
    main()
