#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from guitarfan.extensions.flasksqlalchemy import db
from guitarfan.models.tag import Tag
from enums import *


# tag-tab link table
tag_tab = db.Table('tag_tab',
                   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), index=True),
                   db.Column('tab_id', db.Integer, db.ForeignKey('tab.id', ondelete='CASCADE'), index=True))

class Tab(db.Model):
    __tablename__ = 'tab'

    id = db.Column(db.String(50), primary_key=True, unique=True)
    title = db.Column(db.String(50), nullable=False)
    audio_url = db.Column(db.String)
    format_id = db.Column(db.Integer, nullable=False)
    difficulty_id = db.Column(db.Integer, nullable=False, default=1)
    style_id = db.Column(db.Integer, nullable=False, default=1)
    artist_id = db.Column(db.String(50), db.ForeignKey('artist.id'), index=True)
    hits = db.Column(db.Integer, nullable=False, index=True, default=0)
    update_time = db.Column(db.String(20), nullable=False, index=True)
    tags = db.relationship('Tag', secondary=tag_tab, backref='tabs', lazy='dynamic', passive_deletes=True)
    tabfiles = db.relationship('TabFile', backref='tab', cascade='all,delete-orphan', lazy='dynamic', passive_deletes=True)

    def __init__(self, id, title, format_id, artist_id, difficulty_id, style_id, audio_url, tags):
        self.id = id
        self.title = title
        self.format_id = format_id
        self.artist_id = artist_id
        self.difficulty_id = difficulty_id
        self.style_id = style_id
        self.audio_url = audio_url
        self.hit = 0
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        if tags:
            self.set_tags(tags)


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

    def set_tags(self, value):
        if self.tags:
            for tag in self.tags:
                self.tags.remove(tag)
            if value:
                for tag in value:
                    self.append_tag(tag)

    def append_tag(self, tag):
        if tag and isinstance(tag, Tag):
            # reload tag by id to void error that <object xxx is already attached in session>
            renew_tag = Tag.query.get(tag.id)
            if tag:
                self.tags.append(renew_tag)