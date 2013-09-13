#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid1
from random import random

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask.ext.login import login_user, logout_user, login_required

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db
from guitarfan.utilities import oshelper, validator
from guitarfan.utilities.datatables import ColumnDT, DataTables
from forms.artist import *

bp_admin_artist = Blueprint('bp_admin_artist', __name__, template_folder="../../templates/admin/tabs")


@bp_admin_artist.route('/admin/artists')
@login_required
def list():
    artists = Artist.query.all()
    return render_template('artist_management.html', action='list', artists=artists)


@bp_admin_artist.route('/admin/artists.dataTables_json')
@login_required
def list_dataTables_json():
    # defining columns
    columns = []
    columns.append(ColumnDT('letter', None, col_letter))
    columns.append(ColumnDT('name'))
    columns.append(ColumnDT('region_id', None, col_region))
    columns.append(ColumnDT('category_id', None, col_category))
    columns.append(ColumnDT('id', None, col_tabs))
    columns.append(ColumnDT('id', None, col_photo))
    columns.append(ColumnDT('update_time'))
    columns.append(ColumnDT('id', None, col_operations))

    # defining the initial query
    query = Artist.query

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request, Artist, query, columns)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


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
    artist = Artist.query.get(id)
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
    artist = Artist.query.get(request.values['id'])
    if artist.tabs.count() == 0:
        db.session.delete(artist)
        db.session.commit()
        return 'success'
    else:
        return u"This artist still has tab(s), can't delete"


# dataTables filter methods
def col_letter(letter):
    return '<span class="label label-info">%s</span>' % letter


def col_region(region_id):
    return ArtistRegion.get_item_text(region_id)


def col_category(category_id):
    return ArtistCategory.get_item_text(category_id)


def col_tabs(id):
    total_tabs = Tab.query.filter_by(artist_id=id).count()
    return total_tabs


def col_photo(id):
    artist = Artist.query.get(id)
    if artist and artist.photo and artist.photo != '':
        return '<a href="%s" style="text-decoration: none;" class="preview_link"><i class="icon-eye-open"></i></a>' % artist.photo_relative_path
    else:
        return '<i class="icon-eye-close"></i>'


def col_operations(id):
    html = """
    <div class="dropdown related_menu">
        <a title="Related Objects" class="relate_menu dropdown-toggle" data-toggle="dropdown"><i class="icon icon-list"></i></a>
        <ul class="dropdown-menu pull-right" role="menu">
            <li class="text-left"><a href="%s"><i class="icon-pencil"></i> Edit</a></li>
            <li class="divider"></li>
            <li class="text-left"><a href="%s"><i class="icon-plus"></i> Add Tab</a></li>
    """ % (url_for('bp_admin_artist.edit', id=id), url_for('bp_admin_tab.add', artist_id=id))

    if col_tabs(id) == 0:
        html += """
            <li class="text-left"><a href="javascript:void(0);" onclick="deleteArtist('%s')">
                <i class="icon-remove"></i> Delete</a>
            </li>
        """ % id

    html += """
        </ul>
    </div>
    """

    return html