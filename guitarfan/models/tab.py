#!/usr/bin/env python
# -*- coding: utf-8 -*-

from guitarfan.extensions.flasksqlalchemy import db

# tag-tab link table
tag_tab = db.Table('tag_tab',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('tab_id', db.Integer, db.ForeignKey('tab.id')))

class Tab(db.Model):
    __tablename__ = 'tab'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    format = db.Column(db.Integer)
    hit = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    file_path = db.Column(db.String)
    audio_url = db.Column(db.String)
    style_id = db.Column(db.Integer)
    artist_id = db.Column(db.String(50), db.ForeignKey('artist.id'))
    tags = db.relationship('Tag', secondary=tag_tab, backref=db.backref('tag_tab', lazy='dynamic'))

    def __init__(self, id, name, format, difficulty, file_path, audio_url, style_id, artist_id, tags):
        self.id = id
        self.name = name
        self.format = format
        self.hit = 0
        self.difficulty = difficulty
        self.file_path = file_path
        self.audio_url = audio_url
        self.style_id = style_id
        self.artist_id = artist_id
        self.tags = tags

    def __repr__(self):
        return '<Score %r>' % self.name