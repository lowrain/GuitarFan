#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.login import LoginManager

from guitarfan.models.administrator import Administrator


login_manager = LoginManager()
login_manager.login_view = 'bp_admin_administrator.login'

@login_manager.user_loader
def load_user(id):
    try:
        administrator = Administrator.query.get(id)
    except Exception, e:
        administrator = None
    return administrator
