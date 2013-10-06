#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
# from flask.ext.login import login_user, logout_user, login_required
#
from guitarfan.models import *
# from guitarfan.extensions.flasksqlalchemy import db


bp_frontend_tabs = Blueprint('bp_frontend_tabs', __name__, template_folder="../../templates/site")


@bp_frontend_tabs.route('/tabs')
def tabs():
    letters = map(chr, range(65, 91))
    letters.append('Other')
    regions = ArtistRegion.get_described_items()
    categories = ArtistCategory.get_described_items()
    return render_template('tabs.html', letters=letters, regions=regions, categories=categories)
