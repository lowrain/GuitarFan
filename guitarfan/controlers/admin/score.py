#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from guitarfan.models import *

bp_admin_score = Blueprint('bp_admin_score', __name__, template_folder="admin")

@bp_admin_score.route('/admin/scores', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('admin/score/index.html')
