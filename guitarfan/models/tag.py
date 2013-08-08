#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from guitarfan.extensions.flasksqlalchemy import db

from tab import tag_tab

class Tag(db.Model):
    #finger-style, classic songs, etude, new hot songs
    __tablename__ = 'tag'

    id = db.Column(db.String(50), primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)
    update_time = db.Column(db.String(20))
    tabs = db.relationship('Tab', secondary=tag_tab, lazy='dynamic', passive_deletes=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<Tag %r>' % self.name