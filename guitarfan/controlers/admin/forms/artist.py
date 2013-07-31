#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from flask.ext.wtf import Form, StringField, TextField, HiddenField, BooleanField, PasswordField, SubmitField, \
    SelectField, FileField, HiddenInput, Required, FileAllowed, FileRequired, EqualTo, Regexp, Email, length

from guitarfan.utilities import validator
from guitarfan.models.artist import Artist
from guitarfan.models.enums import *


def get_letter_choices():
    letters = string.uppercase[:26]
    letterChoices = []
    for l in letters:
        letterChoices.append((l, l))

    letterChoices.append(('0', 'Other'))
    return letterChoices


class ArtistFrom(Form):
    id = HiddenField(widget=HiddenInput())
    name = TextField(u'Name', description=u'Unrepeatable.',
                     validators=[Required(message=u'Name is required'), validator.Unique(Artist, Artist.name, message=u'The current name is already in use')])
    letter = SelectField(u'Letter', choices=get_letter_choices())
    photo = FileField(u'Photo', description=u'Upload image file, 120x120.',
                      validators=[validator.AllowedPhotoFile(Artist, Artist.photo, message=u'Upload photo file is not available format')])
    region = SelectField(u'Region', choices=ArtistRegion.get_described_items(), default=1, coerce=int)
    category = SelectField(u'Category', choices=ArtistCategory.get_described_items(), default=1, coerce=int)
    submit = SubmitField(u'Submit', id='submit')
