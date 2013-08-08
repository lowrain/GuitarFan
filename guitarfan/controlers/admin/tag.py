#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid1

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.login import login_required

from guitarfan.extensions.flasksqlalchemy import db
from guitarfan.models import *
from forms.tag import *


bp_admin_tag = Blueprint('bp_admin_tag', __name__, template_folder="../../templates/admin/tabs")


@bp_admin_tag.route('/admin/tags')
@login_required
def list():
    tags = Tag.query.all()
    return render_template('tag_management.html', action='list', tags=tags)


@bp_admin_tag.route('/admin/tags/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TagFrom()
    if request.method == 'GET':
        return render_template('tag_management.html', action='add', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            tag = Tag(str(uuid1()), form.name.data)
            db.session.add(tag)
            db.session.commit()
            flash(u'Add new tag success', 'success')
            return redirect(url_for('bp_admin_tag.list'))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('tag_management.html', action='add', form=form)


@bp_admin_tag.route('/admin/tags/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    tag = Tag.query.filter_by(id=id).first()
    form = TagFrom(id=tag.id, name=tag.name)
    if request.method == 'GET':
        return render_template('tag_management.html', action='edit', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            tag.name = form.name.data
            db.session.commit()
            flash(u'Update tag success', 'success')
            return redirect(url_for('bp_admin_tag.edit', id=id))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('tab_management.html', action='edit', form=form)


@bp_admin_tag.route('/admin/tabgs', methods=['DELETE'])
@login_required
def delete():
    tag_id = request.values['id']
    tag = Tag.query.filter_by(id=tag_id).first()
    db.session.delete(tag)
    db.session.commit()
    return 'success'