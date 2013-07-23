#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, Blueprint


bp_error = Blueprint('bp_error', __name__, template_folder="../templates/error")

@bp_error.app_errorhandler(404)
def page_not_found(error):
     return render_template('404.html')


@bp_error.app_errorhandler(500)
def server_error(error):
    return render_template('500.html')