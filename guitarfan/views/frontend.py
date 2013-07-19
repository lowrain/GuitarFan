#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect, url_for, Blueprint, current_app, session

frontend = Blueprint('frontend', __name__)

