#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, Blueprint
from guitarfan.models import *

admin = Blueprint('admin', __name__)

@admin.route('/')
@admin.route('/admin/')
def admin_index():
    if request.method == 'GET':
        return render_template('admin/index.html')