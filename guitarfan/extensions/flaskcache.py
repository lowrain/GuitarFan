#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.cache import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})