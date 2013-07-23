#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import partial
from flask.ext.principal import Need, Permission


UserAccessNeed = partial(Need, 'functions')


class UserAccessPermission(Permission):

    def __init__(self, name):
        need = UserAccessNeed(name)
        super(UserAccessPermission, self).__init__(need)