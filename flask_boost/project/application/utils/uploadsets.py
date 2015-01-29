# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import uuid
from PIL import Image
from flask.ext.uploads import UploadSet, IMAGES, extension, ALL

# UploadSets
avatars = UploadSet('avatars', IMAGES)


def random_filename():
    """Generate random file name."""
    return str(uuid.uuid4())


def open_image(file_storage):
    """Open image from FileStorage."""
    image = Image.open(file_storage.stream)
    # See: https://github.com/smileychris/easy-thumbnails/issues/95
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image


def save_image(image, upload_set, file_storage):
    """Save image"""
    ext = extension(file_storage.filename)
    filename = '%s.%s' % (random_filename(), ext)
    dir_path = upload_set.config.destination

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    path = os.path.join(dir_path, filename)
    image.save(path)
    return filename


def process_avatar(file_storage, upload_set, max_border):
    """Center clipping, zoom and then save the avatar."""
    image = open_image(file_storage)
    # Center clipping
    w, h = image.size
    if w > h:
        border = h
        avatar_crop_region = ((w - border) / 2, 0, (w + border) / 2, border)
    else:
        border = w
        avatar_crop_region = (0, (h - border) / 2, border, (h + border) / 2)
    image = image.crop(avatar_crop_region)
    # Zoom
    if border > max_border:
        image = image.resize((max_border, max_border), Image.ANTIALIAS)
    filename = save_image(image, upload_set, file_storage)
    return filename
