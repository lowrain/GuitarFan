#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from guitarfan.extensions.flasksqlalchemy import db
from enums import *

# tag-tab link table
tag_tab = db.Table('tag_tab',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('tab_id', db.Integer, db.ForeignKey('tab.id')))

class Tab(db.Model):
    __tablename__ = 'tab'

    id = db.Column(db.String(50), primary_key=True, unique=True)
    title = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String, nullable=False)
    audio_url = db.Column(db.String)
    format_id = db.Column(db.Integer, nullable=False)
    difficulty_id = db.Column(db.Integer, nullable=False, default=1)
    style_id = db.Column(db.Integer, nullable=False, default=1)
    artist_id = db.Column(db.String(50), db.ForeignKey('artist.id'))
    hits = db.Column(db.Integer, nullable=False, default=0)
    update_time = db.Column(db.String(20), nullable=False)
    # tags = db.relationship('Tag', secondary=tag_tab, backref=db.backref('tag_tab', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=tag_tab, backref='tabs', lazy='dynamic')

    def __init__(self, id, title, format_id, artist_id, difficulty_id, style_id, file_path, audio_url):
        self.id = id
        self.title = title
        self.format_id = format_id
        self.artist_id = artist_id
        self.difficulty_id = difficulty_id
        self.style_id = style_id
        self.file_path = file_path
        self.audio_url = audio_url
        self.hit = 0
        # self.tags = tags
        self.update_time = time.strftime('%Y-%m-%d %H:%M')

    def __repr__(self):
        return '<Tab %r>' % self.title

    @property
    def difficulty_text(self):
        return DifficultyDegree.get_item_text(self.difficulty_id)

    @property
    def style_text(self):
        return MusicStyle.get_item_text(self.style_id)

    @property
    def format_text(self):
        return TabFormat.get_item_text(self.format_id)

