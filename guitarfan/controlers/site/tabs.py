#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from sqlalchemy import or_

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db


bp_site_tabs = Blueprint('bp_site_tabs', __name__, template_folder="../../templates/site")


@bp_site_tabs.route('/tabs')
def tabs():
    letters = map(chr, range(65, 91))
    letters.append('0-9')
    letters.append('Other')
    regions = ArtistRegion.get_described_items()
    categories = ArtistCategory.get_described_items()
    return render_template('tabs.html', letters=letters, regions=regions, categories=categories)

@bp_site_tabs.route('/artists.json')
def artists_json():
    letter = request.args['letter']
    artists = []
    for id, name in db.session.query(Artist.id, Artist.name).filter(or_(letter == 'ALL', Artist.letter == letter)):
        artists.append({'id': id, 'name': name})
    return jsonify(artists=artists)