#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from administrator import AdminUser
from artist import Artist
from track import Track
from tab import Score
from enums import *
