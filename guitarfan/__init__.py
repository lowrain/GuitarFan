#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

def create_app(config):
    # init Flask application object
    app = Flask(__name__)
    app.config.from_object(config)

    # init flask-login
    from guitarfan.extensions.flasklogin import login_manager
    login_manager.init_app(app)

    # init flask-sqlalchemy
    from guitarfan.extensions.flasksqlalchemy import db
    db.app = app # if without it, db query operation will throw exception in Form class
    db.init_app(app)

    # register all blueprints
    import controlers
    controlers.Register_Blueprints(app)

    return app
