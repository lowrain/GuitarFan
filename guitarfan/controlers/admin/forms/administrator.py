#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Regexp, Email, Optional, EqualTo

from guitarfan.utilities import validator
from guitarfan.models.administrator import Administrator


class AdministratorLoginForm(Form):
    name = TextField(u'User name or email', validators=[Required(message=u'User name or email is required')])
    password = PasswordField(u'Password', validators=[Required(message=u'Password is required')])
    submit = SubmitField(u'Login', id='submit')


class AddAdministratorForm(Form):
    name = TextField(u'Name', description=u'Unrepeatable.',
                     validators=[Required(message=u'Name is required'),
                                 Regexp(u'^[a-zA-Z0-9\_\-\.\ ]{1,20}$', message=u'Incorrect name format'),
                                 validator.Unique(Administrator, Administrator.name, message=u'The current name is already in use')])
    email = TextField(u'Email', description=u'Unrepeatable.',
                      validators=[Required(message=u'Email is required'),
                                  Email(message=u'Incorrect email format'),
                                  validator.Unique(Administrator, Administrator.email, message=u'The current email is already in use')])
    # group = QuerySelectField(u'Group', description=u'',
    #                          query_factory=Group.query.all, get_label='desc',
    #                          validators=[Required(message=u'Group is required')])
    password = PasswordField(u'Password', description=u'At least eight characters',
                             validators=[Required(message=u'Password is required'),
                                         Regexp(u'^(.{8,20})$', message=u'Password are at least eight chars')])
    confirm_password = PasswordField(u'Confirm Password', description=u'Re-enter the password',
                                     validators=[EqualTo('password', message=u'Passwords must be the same')])
    submit = SubmitField(u'Submit', id='submit')


class EditAdministratorForm(Form):
    new_password = PasswordField(u'New Password', description=u'At least eight characters, if not change please leave it empty',
                                 validators=[Optional(), Regexp(u'^(.{8,20})$', message=u'Password are at least eight chars')])
    confirm_password = PasswordField(u'Confirm Password', description=u'Re-enter the password',
                                     validators=[EqualTo('new_password', message=u'Passwords must be the same')])
    status = BooleanField(u'Status', description=u'Enable')
    submit = SubmitField(u'Submit', id='submit')