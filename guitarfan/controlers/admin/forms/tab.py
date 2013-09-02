#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.fields import TextField, HiddenField, SubmitField, SelectField
from wtforms.widgets import HiddenInput
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import Required, URL, Optional

from guitarfan.models import *


class HackQuerySelectMultipleField(QuerySelectMultipleField):
    def iter_choices(self):
        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), obj.id in [o.id for o in self.data])


class TabFrom(Form):
    id = HiddenField(widget=HiddenInput())
    tab_title = TextField(u'Title', validators=[Required(message=u'Title is required')])
    artist = TextField(u'Artist', validators=[Required(message=u'Artist is required')])
    format = SelectField(u'Format', choices=TabFormat.get_described_items(), default=1, coerce=int)
    difficulty = SelectField(u'Difficulty Degree', choices=DifficultyDegree.get_described_items(), default=1, coerce=int)
    style = SelectField(u'Music Style', choices=MusicStyle.get_described_items(), default=1, coerce=int)
    tags = HackQuerySelectMultipleField(u'Tags', query_factory=Tag.query.all, get_label='name')
    audio_url = TextField(u'Audio Url', validators=[Optional(), URL(message=u'Url is not correct')])
    submit = SubmitField(u'Submit', id='submit')
