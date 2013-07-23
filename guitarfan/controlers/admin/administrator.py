#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid1

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from forms import *

from guitarfan.models.administrator import Administrator
from guitarfan.extensions.flasksqlalchemy import db


bp_admin_administrator = Blueprint('bp_admin_administrator', __name__, template_folder="../../templates/admin")

@bp_admin_administrator.route('/admin/')
@login_required
def index():
    return render_template('index.html')


@bp_admin_administrator.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = AdministratorLoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            administrator = Administrator.query.filter(or_(Administrator.email == form.name.data, Administrator.name == form.name.data)).first()
            if administrator is None:
                flash(u'Account does not exist', 'error')
                return redirect(url_for('bp_admin_administrator.login'))
            elif not administrator.is_active():
                flash(u'Account has been disabled', 'error')
                return redirect(url_for('bp_admin_administrator.login'))
            elif administrator.check_password(form.password.data):
                login_user(administrator)
                flash(u'Welcome ' + administrator.name + ', login successful', 'success')
                return redirect(url_for('bp_admin_administrator.index'))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return redirect(url_for('bp_admin_administrator.index'))


@bp_admin_administrator.route('/admin/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('bp_admin_administrator.login'))


@bp_admin_administrator.route('/admin/administrators')
@login_required
def list():
    administrators = Administrator.query.all()
    return render_template('dashboard/administrator_management.html', action='list', administrators=administrators)

@login_required
@bp_admin_administrator.route('/admin/administrators/add', methods=['GET', 'POST'])
def add():
    form = AddAdministratorForm()

    if request.method == 'GET':
        return render_template('dashboard/administrator_management.html', form=form, action='add')
    elif request.method == 'POST':
        if form.validate_on_submit():
            administrator = Administrator(str(uuid1()), form.name.data, form.email.data, form.password.data, 1)
            db.session.add(administrator)
            db.session.commit()
            flash(u'Creating administrator successfully', 'success')
            return redirect(url_for('bp_admin_administrator.list'))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('dashboard/administrator_management.html', form=form, action='add')


@bp_admin_administrator.route('/admin/administrators/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    administrator = Administrator.query.filter_by(id=id).first()
    form = EditAdministratorForm(status=administrator.status)
    if request.method == 'GET':
        return render_template('dashboard/administrator_management.html', action='edit', form=form, administrator=administrator)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if form.new_password.data:
                administrator.update_password(form.new_password.data)

            administrator.status = form.status.data
            db.session.commit()

            flash('Update administrator successfully', 'success')
            return redirect(url_for('bp_admin_administrator.list'))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('dashboard/administrator_management.html', action='edit', form=form, administrator=administrator)


@bp_admin_administrator.route('/admin/administrators/<string:id>/status/<int:status>', methods=['GET', 'POST'])
@login_required
def update_status(id, status):
    administrator = Administrator.query.filter_by(id=id).first()
    administrator.status = status
    db.session.commit()

    flash('Change administrator status successfully', 'success')
    return redirect(url_for('bp_admin_administrator.list'))

@bp_admin_administrator.route('/admin/administrators/delete/<string:id>')
@login_required
def delete(id):
    administrator = Administrator.query.filter_by(id=id).first()
    db.session.delete(administrator)
    db.session.commit()
    flash(u'Delete administrator successfully', 'success')
    return redirect(url_for('bp_admin_administrator.list'))