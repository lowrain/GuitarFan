#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import shutil
from uuid import uuid1

from flask import render_template, request, current_app, redirect, url_for, flash, Blueprint, jsonify
from flask.ext.login import login_required
from sqlalchemy import exists

from guitarfan.extensions.flasksqlalchemy import db
from guitarfan.utilities import oshelper
from guitarfan.utilities import validator
from guitarfan.models import *
from forms.tab import *

bp_admin_data = Blueprint('bp_admin_data', __name__, template_folder="../../templates/admin/tabs")


@bp_admin_data.route('/admin/data/import', methods=['GET', 'POST'])
@login_required
def data_import():
    if request.method == 'GET':
        return render_template('data_import.html')
    elif request.method == 'POST':
        root_path = request.form['path'] if 'path' in request.form else ''
        result_info = {
            'artists': 0,
            'tabs': 0,
            'errors': []
        }

        # check path
        if root_path == '' or not os.path.isdir(root_path):
            return jsonify(result='failed', msg='invalid path')

        # valid folder names are '0-9', 'other', 'a', 'b', 'c'...'z'
        valid_letter = map(chr, range(97, 123)) + ['0-9', 'other']


        ### Traverse first level folders - letters
        for letter_dir_name in os.listdir(root_path):
            letter_dir_path = os.path.join(root_path, letter_dir_name)
            if not os.path.isdir(letter_dir_path) or not letter_dir_name.lower() in valid_letter:
                continue


            ### Traverse second level folders - artists
            for artist_dir_name in os.listdir(letter_dir_path):
                artist_dir_path = os.path.join(letter_dir_path, artist_dir_name)
                if not os.path.isdir(artist_dir_path):
                    continue

                # create artist if not exist or just fetch it
                artist = Artist.query.filter_by(name=artist_dir_name).first()
                if artist is None:
                    artist = Artist(str(uuid1()), artist_dir_name, '', '', 1, 0)
                    db.session.add(artist)
                    result_info['artists'] += 1


                ## Traverse third level folders - tabs
                for tab_dir_name in os.listdir(artist_dir_path):
                    tab_dir_path = os.path.join(artist_dir_path, tab_dir_name)
                    if not os.path.isdir(tab_dir_path):
                        continue

                    # import tab if not exists
                    if not db.session.query(exists().where(Tab.title == tab_dir_name and Tab.artist_id == artist.id)).scalar():
                        tab = Tab(str(uuid1()), tab_dir_name, 1, artist.id, 1, 1, '', None)
                        db.session.add(tab)
                        result_info['tabs'] += 1


                        ### Traverse imgs files under tab folder
                        for file_name in os.listdir(tab_dir_path):
                            file_path = os.path.join(tab_dir_path, file_name)
                            if not os.path.isfile(file_path):
                                continue

                            if not oshelper.get_extension(file_name) in current_app.config['TAB_FILE_ALLOWED_EXTENSIONS']:
                                continue

                            try:
                                dest_path = os.path.join(oshelper.get_tabfile_upload_abspath(), tab.id)
                                if not os.path.isdir(dest_path):
                                    os.mkdir(dest_path)
                                shutil.copy(file_path, dest_path)

                                tabfile = TabFile(str(uuid1()), tab.id, os.path.join(tab.id, file_name))
                                db.session.add(tabfile)

                            except:
                                e = sys.exc_info()[0]
                                result_info['errors'].append({
                                    'artist': artist_dir_name,
                                    'tab': tab_dir_name,
                                    'file': file_name,
                                    'error': e
                                })
                                continue

                db.session.commit()

    return jsonify(result='success', msg=result_info)