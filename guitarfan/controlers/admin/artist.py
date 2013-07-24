#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid1

from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db
from forms.artist import *

bp_admin_artist = Blueprint('bp_admin_artist', __name__, template_folder="../../templates/admin/tabs")


@bp_admin_artist.route('/admin/artists')
@login_required
def list():
    if request.method == 'GET':
        return render_template('artist_management.html', action='list')


@bp_admin_artist.route('/admin/artist/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddArtistFrom()
    if request.method == 'GET':
        return render_template('artist_management.html', action='add', form=form)

    elif request.method == 'POST':
        file = request.files['photofile']
        if form.validate_on_submit():
            if file and validator.allowed_file(file.filename, 'photo'):
                filename = str(uuid1()) + '.' + file.filename.rsplit('.', 1)[1]
                file.save(current_app.config['ARTIST_PHOTO_FOLDER'] + filename)
            else:
                flash(u'Upload file is not available format', 'error')
                return render_template('artist_management.html', action='add', form=form)

            flash(u'Add new artist successfully', 'success')
            return redirect(url_for('bp_admin_artist.list'))
        else:
            error_message = validator.catch_errors(form.errors)
            if file and not validator.allowed_file(file.filename, 'photo'):
                error_message = error_message.join(';Upload photo is not available image')

            flash(error_message, 'error')
            return render_template('artist_management.html', action='add', form=form)
