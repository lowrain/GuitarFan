#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import flash, current_app
from settings import APP_PATH

def get_abspath(path):
    path = path.lstrip('/')
    return os.path.join(APP_PATH, path)


def get_tabfile_upload_abspath():
    return get_abspath(current_app.config['TAB_FILE_FOLDER'])


def get_artistphoto_upload_abspath():
    return get_abspath(current_app.config['ARTIST_PHOTO_FOLDER'])


def check_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)

def upload_file(file, upload_path, new_filename):
    try:
        check_dir(upload_path)
        file_abspath = os.path.join(upload_path, new_filename)

        file.save(file_abspath)
        return file_abspath
    except Exception as e:
        flash(u'Upload file failed' + e.message + u'. Please try again!', 'warning')
        return ''


def get_extension(fileName):
    filename, extension = os.path.splitext(fileName)
    return extension.lower()