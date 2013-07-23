#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from guitarfan.models import *

bp_admin_tab = Blueprint('bp_admin_tab', __name__, template_folder="../../templates/admin/tabs")


@login_required
@bp_admin_tab.route('/admin/tabs', methods=['GET', 'POST'])
def tab_list():
    if request.method == 'GET':
        return render_template('tab_list.html')
