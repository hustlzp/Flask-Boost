# coding: utf-8
import os
from tempfile import mkstemp
import shutil
import errno


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


src = '/var/www/Flask-Boost/project'
dst = '/tmp/shit'

# 创建项目根文件夹
mkdir_p(dst)

for src_dir, sub_dirs, filenames in os.walk(src):
    if any(substr in src_dir for substr in ['bower_components', 'venv']):
        continue

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
        if any(substr in src_dir for substr in
               ['.pyc', 'config/production.py', 'config/development.py']):
            continue

        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)
        shutil.copy(src_file, dst_file)

        # Create temp file
        fh, abs_path = mkstemp()
        new_file = open(abs_path, 'w')
        old_file = open(src_file)
        for line in old_file:
            new_file.write(line.replace('#{project}', 'shit'))
        # Close temp file
        new_file.close()
        os.close(fh)
        old_file.close()
        # Move new file
        shutil.move(abs_path, dst_file)