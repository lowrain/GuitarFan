#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from uuid import uuid1
from random import random

from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, jsonify
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db
import guitarfan.utilities.oshelper as oshelper
from forms.artist import *

bp_admin_artist = Blueprint('bp_admin_artist', __name__, template_folder="../../templates/admin/tabs")


@bp_admin_artist.route('/admin/artists')
@login_required
def list():
    artists = Artist.query.all()
    return render_template('artist_management.html', action='list', artists=artists)


# TODO move this method to API controller
@bp_admin_artist.route('/admin/artists.json')
@login_required
def list_json():
    if 'q' in request.args:
        artists = Artist.query.filter(Artist.name.like('%'+request.args['q']+'%')).order_by(Artist.name.asc())
    return jsonify(artists=[artist.serialize for artist in artists])


@bp_admin_artist.route('/admin/artists/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ArtistFrom()
    if request.method == 'GET':
        return render_template('artist_management.html', action='add', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            artist_id = str(uuid1())

            # upload photo file
            file = form.photo.data
            photo_filename = ''
            uploadfailed = False

            if file:
                photo_filename = artist_id + '.' + file.filename.rsplit('.', 1)[1]
                if not oshelper.upload_file(file, oshelper.get_artistphoto_upload_abspath(), photo_filename):
                    photo_filename = ''
                    uploadfailed = True

            # add artist to db
            artist = Artist(artist_id, form.name.data, form.letter.data, photo_filename, form.region.data, form.category.data)
            db.session.add(artist)

            # flush data
            db.session.commit()

            flash(u'Add new artist success', 'success')

            if not uploadfailed:
                return redirect(url_for('bp_admin_artist.list'))
            else:
                # flash(u'Upload photo failed. Please try again!', 'warning')
                return redirect(url_for('bp_admin_artist.edit', id=artist_id))
        else:
            error_message = validator.catch_errors(form.errors)
            flash(error_message, 'error')
            return render_template('artist_management.html', action='add', form=form)


@bp_admin_artist.route('/admin/artists/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    artist = Artist.query.filter_by(id=id).first()
    form = ArtistFrom(id=artist.id, name=artist.name, letter=artist.letter, photo=artist.letter,
                      region=artist.region_id, category=artist.category_id)

    photo_relative_path = artist.photo_relative_path + '?dummy=' + str(random())
    if request.method == 'GET':
        return render_template('artist_management.html', action='edit', form=form, photo_path=photo_relative_path)
    elif request.method == 'POST':
        if form.validate_on_submit():
            # update artist
            artist.name = form.name.data
            artist.letter = form.letter.data
            artist.region_id = form.region.data
            artist.category_id = form.category.data

            # upload photo file
            file = form.photo.data
            if file:
                photo_filename = artist.id + '.' + file.filename.rsplit('.', 1)[1]
                if oshelper.upload_file(file, oshelper.get_artistphoto_upload_abspath(), photo_filename):
                    artist.photo = photo_filename

            # flush data
            db.session.commit()

            flash(u'Update artist success', 'success')
            return redirect(url_for('bp_admin_artist.edit', id=id))
        else:
            error_message = validator.catch_errors(form.errors)
            flash(error_message, 'error')
            return render_template('artist_management.html', action='edit', form=form, photo_path=artist.photo_relative_path)


@bp_admin_artist.route('/admin/artists', methods=['DELETE'])
@login_required
def delete():
    artist = Artist.query.filter_by(id=request.values['id']).first()
    if artist.tabs.count() == 0:
        db.session.delete(artist)
        db.session.commit()
        return 'success'
    else:
        return u"This artist still has tab(s), can't delete"
