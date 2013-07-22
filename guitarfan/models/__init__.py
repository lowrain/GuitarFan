#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from administrator import AdminUser
from artist import Artist
from tab import Tab
from tag import Tag
from enums import *
