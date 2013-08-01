#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from guitarfan.extensions.flasksqlalchemy import db

class TabFile(db.Model):
    __tablename__ = 'tabfile'

    id = db.Column(db.String(50), primary_key=True, unique=True)
    filename = db.Column(db.String(200), nullable=False)
    update_time = db.Column(db.String(20), nullable=False)
    tab_id = db.Column(db.String(50), db.ForeignKey('tab.id'))

    def __init__(self, id, tab_id, filename):
        self.id = id
        self.tab_id = tab_id
        self.filename = filename
        self.update_time = time.strftime('%Y-%m-%d %H:%M')

    def __repr__(self):
        return '<TabFile %r %r>' % (self.id, self.filename)