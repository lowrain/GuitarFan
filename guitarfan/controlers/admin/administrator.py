#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from guitarfan.models import *

bp_admin_administrator = Blueprint('bp_admin_administrator', __name__, template_folder="admin")

@bp_admin_administrator.route('/admin/')
def index():
    return render_template('admin/index.html')

@bp_admin_administrator.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    default_next_page = request.values.get('next', url_for('bp_admin_administrator.index'))
    if request.method == 'GET':
        return render_template('admin/administrator/login.html', form=form)
    elif request.method == 'POST':
        if form.name.data == u'' or form.password.data == u'':
            flash(u'Email and password can\'t be empty', 'error')
            return redirect(url_for('admin.login'))
        user = AdminUser.query.filter(or_(AdminUser.email == form.name.data, AdminUser.name == form.name.data)).first()
        if user is not None and not user.is_active():
            flash(u'User has been disabled', 'error')
            return redirect(url_for('bp_admin_administrator.login'))
        elif user is not None and user.check_password(form.password.data):
            login_user(user)
            #identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            flash(u'Login successful', 'success')
            return redirect(default_next_page)
        else:
            flash(u'Incorrect email or password', 'error')
            return redirect(url_for('bp_admin_administrator.login'))





# forms -----------------------------------------------------------------------------
class UserLoginForm(Form):
    next_page = HiddenField()
    name = TextField()
    password = PasswordField()
    submit = SubmitField(u'Login', id='submit')


class CreateUserForm(Form):
    next_page = HiddenField()
    name = TextField(u'UserName <span class="required">*</span>', id='name',
                         description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    email = TextField(u'Email  <span class="required">*</span>', id='email', description=u'Unrepeatable')
    password = PasswordField(u'Password  <span class="required">*</span>', id='password', description=u'At least eight')
    confirm_password = PasswordField(u'Confirm Password  <span class="required">*</span>',
                                     id='confirm_password', description=u'Re-enter the password')
    status = SelectField(u'Status  <span class="required">*</span>', id='status', choices=[(0, u'禁用'), (1, u'启用')])
    submit = SubmitField(u'Submit', id='submit')

class EditUserForm(Form):
    next_page = HiddenField()
    name = TextField(u'UserName <span class="required">*</span>', id='name',
                         description=u'Unrepeatable. REGEX: <code>\'^[a-zA-Z0-9\_\-\.]{1,20}$\'</code>')
    email = TextField(u'Email <span class="required">*</span>', id='email', description=u'Unrepeatable')
    password = PasswordField(u'Password  <span class="required">*</span>', id='password')
    new_password = PasswordField(u'New Password <span class="required">*</span>',
                                 id='new_password', description=u'At least eight')
    confirm_password = PasswordField(u'Confirm Password <span class="required">*</span>',
                                     id='confirm_password', description=u'Re-enter the new password')
    status = SelectField(u'Status  <span class="required">*</span>', id='status', choices=[(0, u'禁用'), (1, u'启用')])
    submit = SubmitField(u'Submit', id='submit')