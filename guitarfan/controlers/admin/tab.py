#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid1

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db
from forms.tab import *
from guitarfan.utilities.oshelper import *
from guitarfan.utilities.qqFileUploader import qqFileUploader

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
    elif request.method == 'POST':
        if form.validate_on_submit():
            tab = Tab(str(uuid1()), form.tab_title.data, form.format.data, form.artist.data.id, form.difficulty.data,
                      form.style.data, u'', form.audio_url.data,)
            db.session.add(tab)
            db.session.commit()
            flash(u'Add new tab successfully', 'success')
            return redirect(url_for('bp_admin_tab.list'))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('tab_management.html', action='add', form=form)


@bp_admin_tab.route('/admin/tabs/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    # TODO implement edit view
    return render_template('tab_management.html')


@bp_admin_tab.route('/admin/tabs/upload', methods=['POST'])
@login_required
def uploadtab():
    # TODO implement upload logic
    if request.method == 'POST':
        uploader = qqFileUploader(request, get_tabfile_upload_abspath(), [".jpg", ".jpeg", ".gif", ".png"])
	return uploader.handleUpload()


# @csrf_exempt
# def upload_delete(request, need_to_delete):
#
# 	qqFileUploader.deleteFile(need_to_delete)
#
# 	return HttpResponse("ok")


@bp_admin_tab.route('/admin/tabs', methods=['DELETE'])
@login_required
def delete():
    tab = Tab.query.filter_by(id=request.values['id']).first()
    db.session.delete(tab)
    db.session.commit()
    return 'success'
