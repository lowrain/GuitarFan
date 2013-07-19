#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db

class Score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.String(32), primary_key=True)
    path = db.Column(db.String(50))
    technique = db.Column(db.Integer)
    format = db.Column(db.Integer)
    hit = db.Column(db.Integer)
    track_id = db.Column(db.String(32), db.ForeignKey('track.id'))

    def __init__(self, id, path, technique, format, track_id):
        self.id = id
        self.path = path
        self.technique = technique
        self.format = format
        self.track_id = track_id

    def __repr__(self):
        return '<Score %r>' % self.id + " : " + self.path