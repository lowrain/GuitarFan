#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify, current_app
from sqlalchemy import func, or_

from guitarfan.models import *
from guitarfan.extensions.flasksqlalchemy import db

bp_site_videos = Blueprint('bp_site_videos', __name__, template_folder="../../templates/site")


@bp_site_videos.route('/videos')
def videos():
     return render_template('coming.html')