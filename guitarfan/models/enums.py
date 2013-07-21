#!/usr/bin/env python
# -*- coding: utf-8 -*-

# domain enum classes
class ArtistCategory(object):
    male = 1
    female = 2
    group = 3
    band = 4
    other = 5

class ArtistRegion(object):
    hl = 1
    ht = 2
    jk = 3
    ue = 4
    other = 0

class MusicStyle(object):
    pop = 1
    rock = 2
    fork = 3
    rnb = 4
    blues = 5
    classic = 6
    country = 7
    jazz = 8
    children = 9
    national = 10
    lover = 11
    other = 0

class PlayTech(object):
    finger = 1
    picker = 2
    other = 0

class ScoreFormat(object):
    img = 1,
    txt = 2,
    gtp = 3,
    other = 4