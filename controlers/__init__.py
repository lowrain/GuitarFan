#!/usr/bin/env python
# -*- coding: utf-8 -*-

from controlers.admin import admin
# from controlers.site import site
# from controlers.api import api

def reg_blueprints(app):
    app.register_blueprint(admin)
    # app.register_blueprint(site)
    # app.register_blueprint(api)