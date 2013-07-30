#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db
from forms.tab import *


bp_admin_tab = Blueprint('bp_admin_tab', __name__, template_folder="../../templates/admin/tabs")


@bp_admin_tab.route('/admin/tabs')
@login_required
def list():
    tabs = Tab.query.all()
    return render_template('tab_management.html', action='list', tabs=tabs)


@bp_admin_tab.route('/admin/tabs/add', methods=['GET', 'POST'])
@login_required
def add():
    # TODO implement add view
    form = TabFrom()
    if request.method == 'GET':
        return render_template('tab_management.html', action='add', form=form)



@bp_admin_tab.route('/admin/tabs/<string:id>', methods=['GET', 'POST'])
@login_required
def edit():
    # TODO implement edit view
    return render_template('tab_management.html')


@bp_admin_tab.route('/admin/tabs', methods=['DELETE'])
@login_required
def delete():
    tab = Tab.query.filter_by(id=request.values['id']).first()
    db.session.delete(tab)
    db.session.commit()
    return 'success'
