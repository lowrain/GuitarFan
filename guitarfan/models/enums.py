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
    child = 9
    national = 10
    other = 0

class DifficultyDegree(object):
    beginner = 1
    Intermediate = 2
    Advanced = 3

class TabFormat(object):
    img = 1,
    txt = 2,
    gtp = 3,
    other = 4