#!/usr/bin/env python
# -*- coding: utf-8 -*-


from uuid import uuid4

from flask import render_template, request, Blueprint, jsonify
from flask.ext.login import login_required

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db
from forms.tab import *
from guitarfan.utilities.oshelper import *
from guitarfan.utilities.qqFileUploader import qqFileUploader


bp_admin_tabfile = Blueprint('bp_admin_tabfile', __name__, template_folder="../../templates/admin/tabs")


@bp_admin_tabfile.route('/admin/tabfiles/<string:tab_id>', methods=['GET', 'PUT'])
@login_required
def edit(tab_id):
    tab = Tab.query.get(tab_id)
    if request.method == 'GET':
        if 'show_wizard' in request.args:
            return render_template('tabfile_edit.html', tab=tab, show_wizard=request.args['show_wizard'])
        else:
            return render_template('tabfile_edit.html', tab=tab)
    elif request.method == 'PUT':
        tabfile = TabFile(str(uuid4()), tab_id, request.form['filename'])
        db.session.add(tabfile)
        db.session.commit()
        tabfiles = TabFile.query.filter_by(tab_id=tab_id).all()
        return jsonify(tabfiles=[tabfile.serialize for tabfile in tabfiles])


@bp_admin_tabfile.route('/admin/tabfiles', methods=['DELETE'])
@login_required
def delete():
    tabfile = TabFile.query.get(request.values['id'])
    db.session.delete(tabfile)
    db.session.commit()
    try:
        if os.path.isfile(tabfile.file_abspath):
            os.remove(tabfile.file_abspath)
    except Exception as e:
        return '%s: %s' % ('error:', e.message)
    return 'success'


# TODO move this method to API controller when implementing API
@bp_admin_tabfile.route('/admin/tabfiles.json')
@login_required
def list_json():
    if 'tab_id' in request.args:
        tabfiles = TabFile.query.filter_by(tab_id=request.args['tab_id']).order_by(TabFile.filename.asc())
        return jsonify(tabfiles=[tabfile.serialize for tabfile in tabfiles])
    else:
        return jsonify(tabfiles=[])


@bp_admin_tabfile.route('/admin/tabfiles/upload/<string:tab_id>', methods=['POST'])
@login_required
def upload(tab_id):
    if request.method == 'POST':
        uploader = qqFileUploader(request, os.path.join(get_tabfile_upload_abspath(), str(tab_id)),
                                  current_app.config['TAB_FILE_ALLOWED_EXTENSIONS'])
    return uploader.handleUpload()