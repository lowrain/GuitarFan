#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask.ext.cache import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode('utf-8')