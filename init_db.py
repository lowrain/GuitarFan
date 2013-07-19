#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

# model classes here
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(50))
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

class Score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.String(32), primary_key=True)
    path = db.Column(db.String(50))
    technique = db.Column(db.Integer)
    format = db.Column(db.Integer)
    track_id = db.Column(db.String(32), db.ForeignKey('track.id'))

    def __init__(self, id, path, technique, format, track_id):
        self.id = id
        self.path = path
        self.technique = technique
        self.format = format
        self.track_id = track_id

    def __repr__(self):
        return '<Score %r>' % self.id + " : " + self.path

class Track(db.Model):
    __tablename__ = 'track'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(50))
    style = db.Column(db.Integer)
    artist_id = db.Column(db.String(32), db.ForeignKey('artist.id'))
    scores = db.relationship('Score', backref='score', lazy='dynamic')

    def __init__(self, id, name, style, artist_id):
        self.id = id
        self.name = name
        self.style = style
        self.artist_id = artist_id

    def __repr__(self):
        return '<Track %r>' % self.name

######################


db.create_all()

