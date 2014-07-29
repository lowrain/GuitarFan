#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import current_app

from time import strftime
from guitarfan.extensions.flasksqlalchemy import db
from guitarfan.utilities.oshelper import *


# def dump_datetime(value):
#     """Deserialize datetime object into string form for JSON processing."""
#     if value is None:
#         return None
#     return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]



class TabFile(db.Model):
    __tablename__ = 'tabfile'

    id = db.Column(db.String(50), primary_key=True, unique=True)
    filename = db.Column(db.String(200), nullable=False)
    update_time = db.Column(db.String(20), nullable=False)
    tab_id = db.Column(db.String(50), db.ForeignKey('tab.id', ondelete='CASCADE'))

    def __init__(self, id, tab_id, filename):
        self.id = id
        self.tab_id = tab_id
        self.filename = filename
        self.update_time = strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<TabFile %r %r>' % (self.id, self.file_basename)

    @property
    def file_relpath(self):
        return os.path.join(current_app.config['TAB_FILE_FOLDER'], self.tab_id, self.filename)

    @property
    def file_abspath(self):
        return os.path.join(get_tabfile_upload_abspath(), self.tab_id, self.filename)

    @property
    def file_basename(self):
        return self.filename.split('/')[-1]

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'id': self.id,
                'tab_id': self.tab_id,
                'update_time': self.update_time,
                'file_basename': self.file_basename,
                'file_relpath': self.file_relpath}
