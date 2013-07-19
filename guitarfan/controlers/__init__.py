#!/usr/bin/env python
# -*- coding: utf-8 -*-

from admin import *

def Register_Blueprints(app):
    app.register_blueprint(bp_admin_administrator)
    app.register_blueprint(bp_admin_score)