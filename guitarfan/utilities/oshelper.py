#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import flash
from settings import APP_PATH

def get_abspath(path):
    path = path.lstrip('/')
    return os.path.join(APP_PATH, path)


def check_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)


def upload_file(file, upload_path, new_filename):
    try:
        upload_folder = get_abspath(upload_path)
        check_dir(upload_folder)
        file_abspath = os.path.join(upload_folder, new_filename)

        # if os.path.isfile(file_abspath):
        #     os.remove(file_abspath)

        file.save(file_abspath)
        return file_abspath
    except Exception as e:
        flash(u'Upload file failed' + e.message + u'. Please try again!', 'warning')
        return ''