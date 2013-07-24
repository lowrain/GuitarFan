#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

# from flask.ext.uploads import UploadSet, IMAGES
from flask.ext.wtf import Form, TextField, HiddenField, BooleanField, PasswordField, SubmitField, SelectField, FileField, \
    Required, FileAllowed, FileRequired, EqualTo, Regexp, Email, length

from guitarfan.utilities import validator
from guitarfan.models.artist import Artist
from guitarfan.models.enums import *


def GetLetterChoices():
    letters = string.uppercase[:26]
    letterChoices = []
    for l in letters:
        letterChoices.append((l, l))

    letterChoices.append(('0', 'Other'))
    return letterChoices

# images = UploadSet("images", IMAGES)

class AddArtistFrom(Form):
    name = TextField(u'Name', description=u'Unrepeatable.',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_\-\.\ ]{1,20}$', message=u'Incorrect name format'),
                                 validator.Unique(Artist, Artist.name, message=u'The current name is already in use')])
    letter = SelectField(u'Alpha', description=u'Select the first letter of artist name.', choices=GetLetterChoices())
    # photo = FileField(u'Photo', description=u'Upload image file, png/jpg/gif.',
    #                   validators=[Regexp(u'^[^/\\]*.[jpg|jpeg|gif|png]$', message=u'Incorrect file format')])
    # photo = FileField(u'Upload artist photo', description=u'Upload artist photo.', validators=[FileAllowed(images, message=u'Images only!')])
    submit = SubmitField(u'Submit', id='submit')

