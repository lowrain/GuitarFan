#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 lowrain(jinzm1982@gmail.com).
#
#                    Created at 2013/07/18.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# database config
DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'data/sqlite.db')

# web config
PORT = 8888
HOST = '127.0.0.1'
SESSION_PROTECTION = 'strong'
SECRET_KEY = 'b\n\x90\\\x13\x044Q\x9a>\x99v\x08\x8ez[\x11 \x82\x83'
DEBUG = True