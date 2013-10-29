#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify, current_app
from sqlalchemy import func, or_

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db


bp_site_tabview = Blueprint('bp_site_tabview', __name__, template_folder="../../templates/site")

@bp_site_tabview.route('/tabview/<string:tab_id>')
def tab_view(tab_id):
    tab = Tab.query.get(tab_id)
    return render_template('tabview.html', tab=tab)