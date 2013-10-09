#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from sqlalchemy import func

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db


bp_frontend_index = Blueprint('bp_frontend_index', __name__, template_folder="../../templates/site")


@bp_frontend_index.route('/')
@bp_frontend_index.route('/index')
def index():
    hot_tabs = Tab.query.order_by(Tab.hits.desc()).limit(10)
    new_tabs = Tab.query.order_by(Tab.update_time.desc()).limit(10)
    return render_template('index.html', hot_tabs=hot_tabs, new_tabs=new_tabs)

@bp_frontend_index.route('/tagcloud.json')
def tag_cloud_json():
    tags = []
    for tag_id, tag_name, tab_count in db.session.query(Tag.id, Tag.name, func.count(Tab.id)).join(Tab).group_by(Tag.id):
        tags.append({'tagId': tag_id, 'tagName': tag_name, 'count': tab_count})
    return jsonify(tags=tags)

@bp_frontend_index.route('/stylecloud.json')
def style_cloud_json():
    styles = []
    for style_id, style_name, tab_count in db.session.query(Tab.style_id, Tab.style_text, func.count(Tab.id)).group_by(Tab.style_id):
        styles.append({'styleId': style_id, 'styleName': style_name, 'count': tab_count})
    return jsonify(styles=styles)