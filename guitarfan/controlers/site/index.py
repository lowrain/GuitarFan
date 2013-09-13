#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
# from flask.ext.login import login_user, logout_user, login_required
#
# from guitarfan.models import *
# from guitarfan.extensions.flasksqlalchemy import db


bp_frontend_index = Blueprint('bp_frontend_index', __name__, template_folder="../../templates/site")


@bp_frontend_index.route('/')
@bp_frontend_index.route('/index')
def index():
    return render_template('index.html')