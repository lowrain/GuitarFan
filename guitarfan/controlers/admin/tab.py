#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from uuid import uuid1
import shutil

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.login import login_required

from guitarfan.extensions.flasksqlalchemy import db
from guitarfan.utilities import oshelper
from guitarfan.utilities import validator
from guitarfan.models import *
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
    artist_id = request.args['artist_id'] if 'artist_id' in request.args else ''
    form = TabFrom(artist=artist_id)
    if request.method == 'GET':
        return render_template('tab_management.html', action='add', form=form,
                               artist=Artist.query.filter_by(id=artist_id).first())
    elif request.method == 'POST':
        if form.validate_on_submit():
            tab = Tab(str(uuid1()), form.tab_title.data, form.format.data, form.artist.data, form.difficulty.data,
                      form.style.data, form.audio_url.data, form.tags.data)
            db.session.add(tab)
            db.session.commit()
            flash(u'Add new tab success, please upload tab files', 'success')
            return redirect(url_for('bp_admin_tabfile.edit', tab_id=tab.id, show_wizard=True))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('tab_management.html', action='add', form=form)


@bp_admin_tab.route('/admin/tabs/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    tab = Tab.query.get(id)
    form = TabFrom(id=tab.id, tab_title=tab.title, format=tab.format_id, difficulty=tab.difficulty_id,
                   style=tab.style_id, audio_url=tab.audio_url, tags=tab.tags, artist=tab.artist_id)
    if request.method == 'GET':
        return render_template('tab_management.html', action='edit', form=form, artist=tab.artist)
    elif request.method == 'POST':
        if form.validate_on_submit():
            tab.title = form.tab_title.data
            tab.format_id = form.format.data
            tab.difficulty_id = form.difficulty.data
            tab.style_id = form.style.data
            tab.artist_id = form.artist.data
            tab.audio_url = form.audio_url.data
            tab.set_tags(form.tags.data)
            db.session.commit()
            flash(u'Update tab success', 'success')
            return redirect(url_for('bp_admin_tab.edit', id=id))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('tab_management.html', action='edit', form=form)


@bp_admin_tab.route('/admin/tabs', methods=['DELETE'])
@login_required
def delete():
    if 'id' not in request.values:
        return 'invalid id'

    tab_id = request.values['id']
    tab = Tab.query.get(tab_id)
    db.session.delete(tab)
    db.session.commit()

    try:
        tabfiles_folder_path = os.path.join(oshelper.get_tabfile_upload_abspath(), tab_id)
        if os.path.isdir(tabfiles_folder_path):
            shutil.rmtree(tabfiles_folder_path)
    except Exception as e:
        return '%s: %s' % ('error:', e.message)
    return 'success'