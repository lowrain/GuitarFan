#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from guitarfan.models import *

bp_admin_tag = Blueprint('bp_admin_tag', __name__, template_folder="../../templates/admin/tabs")


@bp_admin_tag.route('/admin/tags')
@login_required
def list():
    if request.method == 'GET':
        return render_template('tag_management.html', action='list')


@bp_admin_tag.route('/admin/tags/add', methods=['GET', 'POST'])
@login_required
def add():
    return render_template('tag_management.html')
