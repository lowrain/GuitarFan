#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

def create_app(config):
    # init Flask application object
    app = Flask(__name__)
    app.config.from_object(config)

    # init sqlalchemy db
    from models import db
    db.init_app(app)

    # register all views in blueprint
    from views import admin, api, frontend
    app.register_blueprint(admin)
    app.register_blueprint(api)
    app.register_blueprint(frontend)

    return app
