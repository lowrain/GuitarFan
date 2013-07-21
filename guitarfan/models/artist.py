#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(50))
    alpha = db.Column(db.String(1))
    photo = db.Column(db.String)
    region_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    tracks = db.relationship('Track', backref='track', lazy='dynamic')

    def __init__(self, id, name, region_id, category_id):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.region_id = region_id

    def __repr__(self):
        return '<Artist %r>' % self.name