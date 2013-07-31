#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from flask.ext.wtf import Form, StringField, TextField, HiddenField, BooleanField, PasswordField, SubmitField, \
    SelectField, FileField, QuerySelectField, QuerySelectMultipleField, HiddenInput, Required, URL, Optional, \
    FileAllowed, FileRequired, EqualTo, Regexp, Email, length

from guitarfan.utilities import validator
from guitarfan.models import *


class TabFrom(Form):
    id = HiddenField(widget=HiddenInput())
    tab_title = TextField(u'Title', validators=[Required(message=u'Title is required')])
    artist = QuerySelectField(u'Artist', query_factory=Artist.query.all, get_label='name',
                              validators=[Required(message=u'Artist is required')])
    format = SelectField(u'Format', choices=TabFormat.get_described_items(), default=1, coerce=int)
    difficulty = SelectField(u'Difficulty Degree', choices=DifficultyDegree.get_described_items(), default=1, coerce=int)
    style = SelectField(u'Music Style', choices=MusicStyle.get_described_items(), default=1, coerce=int)
    tags = QuerySelectMultipleField(u'Tags', query_factory=Tag.query.all)
    audio_url = TextField(u'Audio Url', validators=[Optional(), URL(message=u'Url is not correct')])
    submit = SubmitField(u'Submit', id='submit')
