#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify, current_app
from sqlalchemy import func, or_

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db
from guitarfan.extensions.flaskcache import cache, make_cache_key


bp_site_tabs = Blueprint('bp_site_tabs', __name__, template_folder="../../templates/site")


@bp_site_tabs.route('/tabs')
@bp_site_tabs.route('/tabs/<int:page>')
@cache.cached(3600, key_prefix=make_cache_key)
def tabs(page = 1):
    if 'artist' in request.args:
        artist_id = request.args['artist']
        artist = Artist.query.get(artist_id)
        tabs = Tab.query.filter(Tab.artist_id == artist_id).order_by('update_time desc').paginate(page, current_app.config['TABS_PER_PAGE'], True)
        return render_template('tabs.html', tabs=tabs, artist=artist, mode='artist')
    elif 'style' in request.args:
        style_id = int(request.args['style'])
        style = enums.MusicStyle.get_item_text(style_id)
        tabs = Tab.query.filter(Tab.style_id == style_id).order_by('update_time desc').paginate(page, current_app.config['TABS_PER_PAGE'], True)
        return render_template('tabs.html', tabs=tabs, style=style, mode='style')
    elif 'tag' in request.args:
        tag_id = request.args['tag']
        tag = Tag.query.get(tag_id)
        tabs = Tab.query.join(Tab.tags).filter(Tag.id == tag_id).order_by('Tab.update_time desc').paginate(page, current_app.config['TABS_PER_PAGE'], True)
        return render_template('tabs.html', tabs=tabs, tag=tag, mode='tag')
    # TODO search mode
    elif 'search' in request.args:
        # TODO limit match entire english word not single letter
        search = request.args['search']
        tabs = Tab.query.join(Artist).filter(or_(Tab.title.like('%' + search + '%'), Artist.name.like('%' + search + '%')))\
            .order_by('Tab.update_time desc').paginate(page, current_app.config['TABS_PER_PAGE'], True)
        return render_template('tabs.html', tabs=tabs, mode='search')
    else:
        letters = map(chr, range(65, 91))
        letters.append('0-9')
        letters.append('Other')
        regions = ArtistRegion.get_described_items()
        categories = ArtistCategory.get_described_items()

        order_by = 'update_time'
        if 'order' in request.args and request.args['order'] == 'hot':
            order_by = 'hits'

        tabs = Tab.query.order_by(order_by + ' desc').paginate(page, current_app.config['TABS_PER_PAGE'], True)
        return render_template('tabs.html', letters=letters, regions=regions, categories=categories, tabs=tabs, mode='list')


@bp_site_tabs.route('/artists.json', methods=['POST'])
def artists_json():
    letter = request.form['queryFilter[artistLetter]']
    category_id = int(request.form['queryFilter[artistCategoryId]'])
    region_id = int(request.form['queryFilter[artistRegionId]'])
    artists = []
    for id, name, category in db.session.query(Artist.id, Artist.name, Artist.category_id) \
        .filter(or_(Artist.letter == letter)) \
        .filter(or_(category_id == 0, Artist.category_id == category_id)) \
        .filter(or_(region_id == 0, Artist.region_id == region_id)) \
        .order_by('category_id'):
        artists.append({'id': id, 'name': name, 'category': category})
    return jsonify(artists=artists)


@bp_site_tabs.route('/tabs.json', methods=['POST'])
def tabs_json():
    letter = request.form['queryFilter[artistLetter]']
    category_id = int(request.form['queryFilter[artistCategoryId]'])
    region_id = int(request.form['queryFilter[artistRegionId]'])
    order_by = 'Tab.update_time' if request.form['queryFilter[orderBy]'] == 'time' else 'Tab.hits'
    artists = request.form['queryFilter[artistIds]'].split('|') if request.form['queryFilter[artistIds]'] != '' else []
    style_id = int(request.form['queryFilter[styleId]'])
    tag_id = request.form['queryFilter[tagId]']
    search = request.form['queryFilter[search]']
    page_index = int(request.form['queryFilter[pageIndex]'])
    tabs = []

    page_size = current_app.config['TABS_PER_PAGE']

    count_query = db.session.query(func.count(Tab.id)).join(Artist)
    tab_query = db.session.query(Tab.id, Tab.title, Tab.style_id, Tab.difficulty_id, Tab.hits, Tab.artist_id, Artist.name).join(Artist)

    if letter != 'All':
        tab_query = tab_query.filter(Artist.letter == letter)
        count_query = count_query.filter(Artist.letter == letter)
    if category_id > 0:
        tab_query = tab_query.filter(Artist.category_id == category_id)
        count_query = count_query.filter(Artist.category_id == category_id)
    if region_id > 0:
        tab_query = tab_query.filter(Artist.region_id == region_id)
        count_query = count_query.filter(Artist.region_id == region_id)
    if len(artists) > 0:
        tab_query = tab_query.filter(Artist.id.in_(artists))
        count_query = count_query.filter(Artist.id.in_(artists))
    if style_id > 0:
        tab_query = tab_query.filter(Tab.style_id == style_id)
        count_query = count_query.filter(Tab.style_id == style_id)
    if tag_id != '':
        tab_query = tab_query.join(Tab.tags).filter(Tag.id == tag_id)
        count_query = count_query.join(Tab.tags).filter(Tag.id == tag_id)
    if search != '':
        tab_query = tab_query.filter(or_(Tab.title.like('%' + search + '%'), Artist.name.like('%' + search + '%')))
        count_query = count_query.filter(or_(Tab.title.like('%' + search + '%'), Artist.name.like('%' + search + '%')))

    page_count = math.ceil(float(count_query.scalar())/page_size)
    tab_query = tab_query.order_by(order_by + ' desc').limit(page_size).offset(page_size * (page_index - 1))

    for id, title, style_id, difficalty_id, hits, artist_id, artist_name in tab_query:
        tabs.append({
            'id': id,
            'title': title,
            'style': MusicStyle.get_item_text(style_id),
            'difficalty': DifficultyDegree.get_item_text(difficalty_id),
            'hits': hits,
            'artistId': artist_id,
            'artistName': artist_name
        })

    return jsonify(tabs=tabs, pageIndex=page_index, pageCount=page_count)
