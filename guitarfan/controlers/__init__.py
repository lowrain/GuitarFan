#!/usr/bin/env python
# -*- coding: utf-8 -*-

from admin.administrator import bp_admin_administrator
from admin.artist import bp_admin_artist
from admin.tag import bp_admin_tag
from admin.tab import bp_admin_tab
from admin.tabfile import bp_admin_tabfile
from admin.data import bp_admin_data
from site.index import bp_frontend_index
from error import bp_error

def Register_Blueprints(app):
    app.register_blueprint(bp_admin_administrator)
    app.register_blueprint(bp_admin_artist)
    app.register_blueprint(bp_admin_tag)
    app.register_blueprint(bp_admin_tab)
    app.register_blueprint(bp_admin_tabfile)
    app.register_blueprint(bp_admin_data)
    app.register_blueprint(bp_frontend_index)
    app.register_blueprint(bp_error)