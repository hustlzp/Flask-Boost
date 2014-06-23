# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import uuid
from PIL import Image
from flask.ext.uploads import UploadSet, IMAGES, extension, ALL

# UploadSets
avatars = UploadSet('avatars', IMAGES)


def random_filename():
    """生成伪随机文件名"""
    return str(uuid.uuid4())


def open_image(file_storage):
    """打开图像"""
    image = Image.open(file_storage.stream)
    # 此处是为了修复一个bug：cannot write mode P as JPEG
    # 解决方法来自：https://github.com/smileychris/easy-thumbnails/issues/95
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image


def save_image(image, upload_set, file_storage):
    """保存图片
    保存到upload_set对应的文件夹中
    文件后缀使用file_storage中文件名的后缀
    """
    ext = extension(file_storage.filename)
    filename = '%s.%s' % (random_filename(), ext)
    dir_path = upload_set.config.destination
    # 若不存在此目录，则创建之
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    path = os.path.join(dir_path, filename)
    image.save(path)
    return filename


def process_avatar(file_storage, upload_set, max_border):
    """将上传的头像进行居中裁剪、缩放，然后保存"""
    image = open_image(file_storage)
    # 居中裁剪
    w, h = image.size
    if w > h:
        border = h
        avatar_crop_region = ((w - border) / 2, 0, (w + border) / 2, border)
    else:
        border = w
        avatar_crop_region = (0, (h - border) / 2, border, (h + border) / 2)
    image = image.crop(avatar_crop_region)
    # 缩放
    if border > max_border:
        image = image.resize((max_border, max_border), Image.ANTIALIAS)
    filename = save_image(image, upload_set, file_storage)
    return filename