#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from uuid import uuid4
from settings import APP_PATH
from guitarfan.models.artist import Artist
from guitarfan.models.tab import Tab
from guitarfan.models.tabfile import TabFile
from guitarfan.utilities.pinyin import Pinyin
from guitarfan.extensions.flasksqlalchemy import db
from guitarfan.utilities.oshelper import *

def update_tabfile_filename():
    pinyin = Pinyin()
    # tabfiles = TabFile.query.all()
    # for tabfile in tabfiles:
    #     old_file_name = os.path.basename(tabfile.filename)
    #     new_file_name = pinyin.get_initials(old_file_name)
    #
    #     # update files name
    #     new_file_path = os.path.join(get_tabfile_upload_abspath(), tabfile.tab_id, new_file_name)
    #     fileexists = os.path.exists(tabfile.file_abspath)
    #     isfile = os.path.isfile(tabfile.file_abspath)
    #     #os.rename(tabfile.file_abspath, new_file_path)
    #
    #     # update tabfile table
    #     #tabfile.filename = tabfile.id + '/' + new_file_name
    #
    # #db.session.commit()

    tabs = Tab.query.all()
    for tab in tabs:
        tab_title_pinyin = pinyin.get_initials(tab.title).lower()
        tabfile_dir = os.path.join(get_tabfile_upload_abspath(), tab.id)

        if not os.path.exists(tabfile_dir):
            continue

        tabfiles = os.listdir(tabfile_dir)
        if len(tabfiles) == 1:
            old_fullpath = os.path.join(tabfile_dir, tabfiles[0])
            new_fullpath = os.path.join(tabfile_dir, tab_title_pinyin + get_extension(tabfiles[0]))
            os.rename(old_fullpath, new_fullpath)
        elif len(tabfiles) > 1:
            i = 0
            for filename in tabfiles:
                i += 1
                old_fullpath = os.path.join(tabfile_dir, filename)
                new_fullpath = os.path.join(tabfile_dir, tab_title_pinyin + str(i) + get_extension(filename))
                os.rename(old_fullpath, new_fullpath)
    return

def update_tabfile_table():
    tabs = Tab.query.all()
    for tab in tabs:
        tabfile_dir = os.path.join(get_tabfile_upload_abspath(), tab.id)

        if not os.path.exists(tabfile_dir):
            continue

        tabfiles = os.listdir(tabfile_dir)

        if len(tabfiles) >= 1:
            for filename in tabfiles:
                tabfile = TabFile(str(uuid4()), tab.id, filename)
                db.session.add(tabfile)
                db.session.commit()
    return