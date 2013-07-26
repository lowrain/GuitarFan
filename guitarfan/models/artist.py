#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from flask import url_for, current_app
from guitarfan.extensions.flasksqlalchemy import db
import guitarfan.utilities.oshelper as oshelper

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    letter = db.Column(db.String(1))
    photo = db.Column(db.String)
    region_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    update_time = db.Column(db.String(20))
    tabs = db.relationship('Tab', backref='artist', lazy='dynamic')

    def __init__(self, id, name, letter, photo, region_id, category_id):
        self.id = id
        self.name = name
        self.letter = letter
        self.photo = photo
        self.category_id = category_id
        self.region_id = region_id
        self.update_time = time.strftime('%Y-%m-%d %H:%M')

    def __repr__(self):
        return '<Artist %r>' % self.name

    @property
    def photo_relative_path(self):
        nophoto_path = url_for('static', filename='images/nophoto.png')

        if self.photo == '':
            return nophoto_path

        photo_path = current_app.config['ARTIST_PHOTO_FOLDER'] + '/' + self.photo
        if os.path.isfile(oshelper.get_abspath(photo_path)):
            return photo_path
        else:
            return nophoto_path




