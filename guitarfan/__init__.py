#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

def create_app(config):
    # init Flask application object
    app = Flask(__name__)
    app.config.from_object(config)

    # config Flask-Login
    from guitarfan.extensions.flasklogin import login_manager
    login_manager.init_app(app)

    # init sqlalchemy db
    from guitarfan.extensions.flasksqlalchemy import db
    db.init_app(app)

    # register all blueprints
    import controlers
    controlers.Register_Blueprints(app)

    return app
