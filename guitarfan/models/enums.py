#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator


# domain enum classes
class EnumBase(object):
    _descriptions = {}

    @classmethod
    def get_items(cls):
        # change all enum items to sorted list
        # [(1,'aa'), (2,'bb'), (3,'cc')]
        items_dict = dict((v, k) for k, v in cls.__dict__.items() if not k.startswith('_') and not k.startswith('get_'))
        sorted_list = sorted(items_dict.iteritems(), key=operator.itemgetter(0))
        return sorted_list

    @classmethod
    def get_described_items(cls):
        # get described enum items list which is for displaying to end user
        # [(1,u'描述1'), (2,u'描述2'), (3,u'描述3')]
        items = cls.get_items()
        new_items = []
        for item in items:
            new_items.append((item[0], cls._descriptions[item[0]]))
        return new_items

    @classmethod
    # get the corresponding text for given enum item
    # band ==> u‘乐队'
    def get_item_text(cls, item):
        return cls._descriptions[item]


class ArtistCategory(EnumBase):
    male = 1
    female = 2
    group = 3
    band = 4
    other = 0

    _descriptions = {male: u'男艺人', female: u'女艺人', group: u'组合', band: u'乐队', other: u'其他'}


class ArtistRegion(EnumBase):
    hl = 1
    ht = 2
    jk = 3
    ue = 4
    other = 0

    _descriptions = {hl: u'内地', ht: u'港台', jk: u'日韩', ue: u'欧美', other: u'其他'}


class MusicStyle(EnumBase):
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

    _descriptions = {pop: u'流行', rock: u'摇滚', fork: u'民谣', rnb: u'R&B', blues: u'蓝调', classic: u'古典', country:u'乡村',
                     jazz: u'爵士', child: u'儿歌', national: u'民族', other: u'其他'}

class DifficultyDegree(EnumBase):
    beginner = 1
    intermediate = 2
    advanced = 3

    _descriptions = {beginner: u'入门', intermediate: u'中级', advanced: u'高级'}


class TabFormat(EnumBase):
    img = 1
    txt = 2
    gtp = 3

    _descriptions = {img: u'图片', txt: u'文本', gtp: u'GTP'}