#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db

class Track(db.Model):
    __tablename__ = 'track'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(50))
    style_id = db.Column(db.Integer)
    classic = db.Column(db.Boolean)
    online_url = db.Column(db.String)
    artist_id = db.Column(db.String(32), db.ForeignKey('artist.id'))
    scores = db.relationship('Score', backref='score', lazy='dynamic')

    def __init__(self, id, name, style, artist_id):
        self.id = id
        self.name = name
        self.style = style
        self.artist_id = artist_id

    def __repr__(self):
        return '<Track %r>' % self.name