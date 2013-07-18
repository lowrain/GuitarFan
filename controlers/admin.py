#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import exc
from flask import render_template, request, redirect, url_for, flash, Blueprint

admin = Blueprint('admin', __name__, template_folder='templates/admin')

@admin.route('/')
@admin.route('/admin/')
def admin_index():
    if request.method == 'GET':
       return render_template('admin/index.html')