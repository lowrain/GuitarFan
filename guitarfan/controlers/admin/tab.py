#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid1

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, SubmitField, QuerySelectField, SelectField
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from sqlalchemy.ext.serializer import loads, dumps

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
    # TODO add tags fields
    form = TabFrom()
    if request.method == 'GET':
        return render_template('tab_management.html', action='add', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            tab = Tab(str(uuid1()), form.tab_title.data, form.format.data, form.artist.data.id, form.difficulty.data,
                      form.style.data, form.audio_url.data)
            db.session.add(tab)
            db.session.commit()
            flash(u'Add new tab successfully, please upload tab files', 'success')
            return redirect(url_for('bp_admin_tab.tabfile_edit', tab_id=tab.id, show_wizard=True))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('tab_management.html', action='add', form=form)


@bp_admin_tab.route('/admin/tabs/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    tab = Tab.query.filter_by(id=id).first()
    form = TabFrom(id=tab.id, tab_title=tab.title, format=tab.format_id, difficulty=tab.difficulty_id,
                   style=tab.style_id, tags=tab.tags, audio_url=tab.audio_url)
    if request.method == 'GET':
        return render_template('tab_management.html', action='edit', form=form)
    # TODO implement edit post


@bp_admin_tab.route('/admin/tabs', methods=['DELETE'])
@login_required
def delete():
    tab = Tab.query.filter_by(id=request.values['id']).first()
    db.session.delete(tab)
    db.session.commit()
    return 'success'


@bp_admin_tab.route('/admin/tabfiles/<string:tab_id>', methods=['GET', 'PUT'])
@login_required
def tabfile_edit(tab_id):
    tab = Tab.query.filter_by(id=tab_id).first()
    if request.method == 'GET':
        if 'show_wizard' in request.args:
            return render_template('tabfile_edit.html', tab=tab, show_wizard=request.args['show_wizard'])
        else:
            return render_template('tabfile_edit.html', tab=tab)
    elif request.method == 'PUT':
        filename = os.path.join(tab_id, request.form['filename'])
        tabfile = TabFile(str(uuid1()), tab_id, filename)
        db.session.add(tabfile)
        db.session.commit()
        tabfiles = TabFile.query.filter_by(tab_id=tab_id).all()
        return jsonify(tabfiles=[tabfile.serialize for tabfile in tabfiles])


@bp_admin_tab.route('/admin/tabfiles', methods=['DELETE'])
@login_required
def tabfile_delete():
    tabfile = TabFile.query.filter_by(id=request.values['id']).first()
    db.session.delete(tabfile)
    db.session.commit()
    try:
        if os.path.isfile(tabfile.file_abspath()):
            os.remove(tabfile.file_abspath())
    except Exception as e:
        return '%s: %s' % ('error:', e.message)
    return 'success'


# TODO move this method to API controller when implementing API
@bp_admin_tab.route('/admin/tabfiles.json')
@login_required
def tabfiles_json():
    if 'tab_id' in request.args:
        tabfiles = TabFile.query.filter_by(tab_id=request.args['tab_id']).all()
        return jsonify(tabfiles=[tabfile.serialize for tabfile in tabfiles])
    else:
        return jsonify(tabfiles=[])


@bp_admin_tab.route('/admin/tabfiles/upload/<string:tab_id>', methods=['POST'])
@login_required
def tabfile_upload(tab_id):
    if request.method == 'POST':
        uploader = qqFileUploader(request, os.path.join(get_tabfile_upload_abspath(), str(tab_id)),
                                  current_app.config['TAB_FILE_ALLOWED_EXTENSIONS'])
    return uploader.handleUpload()