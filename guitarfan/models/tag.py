#!/usr/bin/env python
# -*- coding: utf-8 -*-

from guitarfan.extensions.flasksqlalchemy import db

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.String(50), primary_key=True, unique=True)
    name = db.Column(db.String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.name


#finger-style, classic songs, etude, new hot songs