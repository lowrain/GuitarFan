#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify, current_app
from sqlalchemy import or_

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db


bp_site_tabs = Blueprint('bp_site_tabs', __name__, template_folder="../../templates/site")


@bp_site_tabs.route('/tabs')
@bp_site_tabs.route('/tabs/<int:page>')
def tabs(page = 1):
    letters = map(chr, range(65, 91))
    letters.append('0-9')
    letters.append('Other')
    regions = ArtistRegion.get_described_items()
    categories = ArtistCategory.get_described_items()
    tabs = Tab.query.order_by('update_time desc').paginate(page, current_app.config['POSTS_PER_PAGE'], True)
    return render_template('tabs.html', letters=letters, regions=regions, categories=categories, tabs=tabs)


@bp_site_tabs.route('/artists.json', methods=['POST'])
def artists_json():
    letter = request.form['queryFilter[artistLetter]']
    artists = []
    for id, name, category in db.session.query(Artist.id, Artist.name, Artist.category_id).filter(or_(letter == 'ALL', Artist.letter == letter)):
        artists.append({'id': id, 'name': name, 'category': category})
    return jsonify(artists=artists)


@bp_site_tabs.route('/tabs.json')
def tabs_json():
    tabs = []
    for title, styleId, difficaltyId, hits, artistId, artistName \
    in db.session.query(Tab.title, Tab.style_id, Tab.difficulty_id, Tab.hits, Tab.artist_id, Tab.artist.name).order_by('update_time desc'):
        tabs.append({
            'title': title,
            'style': MusicStyle.get_item_text(styleId),
            'difficalty': DifficultyDegree.get_described_items(difficaltyId),
            'hits': hits,
            'artistId': artistId,
            'artistName': artistName
        })
    return jsonify(tabs=tabs)