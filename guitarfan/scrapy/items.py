#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class Artist(Item):
    name = Field()


class Tab(Item):
    name = Field()