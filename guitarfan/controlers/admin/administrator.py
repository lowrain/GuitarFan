#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid1

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from guitarfan.models.administrator import Administrator
from guitarfan.extensions.flasksqlalchemy import db
from forms.administrator import *

bp_admin_administrator = Blueprint('bp_admin_administrator', __name__, template_folder="../../templates/admin")

@bp_admin_administrator.route('/admin')
@login_required
def index():
    return render_template('admin/index.html')


@bp_admin_administrator.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = AdministratorLoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            administrator = Administrator.query.filter(or_(Administrator.email == form.name.data, Administrator.name == form.name.data)).first()
            passed = True
            if administrator is None:
                flash(u'Account does not exist', 'error')
                passed = False
            elif not administrator.is_active():
                flash(u'Account has been disabled', 'error')
                passed = False
            elif administrator.check_password(form.password.data):
                flash(u'Welcome ' + administrator.name + ', login successful', 'success')
                passed = True
            else:
                flash(u'Password is not correct', 'error')
                passed = False

            if passed:
                login_user(administrator)
                if 'next' in request.values:
                    return redirect(request.values['next'])
                else:
                    return redirect(url_for('bp_admin_administrator.list'))
            else:

                return render_template('login.html', form=form)
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('login.html', form=form)


@bp_admin_administrator.route('/admin/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('bp_admin_administrator.login'))


@bp_admin_administrator.route('/admin/administrators')
@login_required
def list():
    administrators = Administrator.query.all()
    return render_template('dashboard/administrator_management.html', action='list', administrators=administrators)


@bp_admin_administrator.route('/admin/administrators/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddAdministratorForm()

    if request.method == 'GET':
        return render_template('dashboard/administrator_management.html', action='add', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            administrator = Administrator(str(uuid1()), form.name.data, form.email.data, form.password.data, 1)
            db.session.add(administrator)
            db.session.commit()
            flash(u'Add new administrator successfully', 'success')
            return redirect(url_for('bp_admin_administrator.list'))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('dashboard/administrator_management.html', action='add', form=form)


@bp_admin_administrator.route('/admin/administrators/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    administrator = Administrator.query.get(id)
    form = EditAdministratorForm(status=administrator.status)
    if request.method == 'GET':
        return render_template('dashboard/administrator_management.html', action='edit', form=form, administrator=administrator)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if 8 <= len(form.new_password.data) <= 20:
                administrator.update_password(form.new_password.data)
            if current_user.name != administrator.name:
                administrator.status = form.status.data
            db.session.commit()

            flash(u'Update administrator successfully', 'success')
            return redirect(url_for('bp_admin_administrator.list'))
        else:
            flash(validator.catch_errors(form.errors), 'error')
            return render_template('dashboard/administrator_management.html', action='edit', form=form, administrator=administrator)


@bp_admin_administrator.route('/admin/administrators', methods=['DELETE'])
@login_required
def delete():
    administrator = Administrator.query.get(request.values['id'])
    db.session.delete(administrator)
    db.session.commit()
    return 'success'


@bp_admin_administrator.route('/admin/administrators/<string:id>/status/<int:status>')
@login_required
def update_status(id, status):
    administrator = Administrator.query.get(id)
    administrator.status = status
    db.session.commit()

    flash('Change administrator status successfully', 'success')
    return redirect(url_for('bp_admin_administrator.list'))
