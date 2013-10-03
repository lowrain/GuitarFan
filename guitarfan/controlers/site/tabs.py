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
    return render_template('tabs.html', letters=letters)