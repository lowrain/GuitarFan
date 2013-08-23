#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from flask import url_for, current_app
from guitarfan.extensions.flasksqlalchemy import db
import guitarfan.utilities.oshelper as oshelper
from enums import *

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.String(50), primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    letter = db.Column(db.String(5))
    photo = db.Column(db.String)
    region_id = db.Column(db.Integer, nullable=False, default=1)
    category_id = db.Column(db.Integer, nullable=False, default=1)
    update_time = db.Column(db.String(20), nullable=False)
    tabs = db.relationship('Tab', backref='artist', cascade='all,delete-orphan', lazy='dynamic')

    def __init__(self, id, name, letter, photo, region_id, category_id):
        self.id = id
        self.name = name
        self.letter = letter
        self.photo = photo
        self.category_id = category_id
        self.region_id = region_id
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return '<Artist %r>' % self.name

    @property
    def region_text(self):
        return ArtistRegion.get_item_text(self.region_id)

    @property
    def category_text(self):
        return ArtistCategory.get_item_text(self.category_id)

    @property
    def photo_relative_path(self):
        nophoto_path = url_for('static', filename='images/nophoto.png')

        if self.photo == '':
            return nophoto_path

        photo_path = os.path.join(current_app.config['ARTIST_PHOTO_FOLDER'], self.photo)
        if os.path.isfile(oshelper.get_abspath(photo_path)):
            return photo_path
        else:
            return nophoto_path

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'id': self.id,
                'name': self.name,
                'letter': self.letter,
                'category_id': self.category_id,
                'category_text': self.category_text,
                'region_id': self.region_id,
                'region_text': self.region_text,
                'photo_relative_path': self.photo_relative_path,
                'update_time': self.update_time}
