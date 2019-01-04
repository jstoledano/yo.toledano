#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *


SITEURL = 'https://yo.toledano.org'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
FEED_MAX_ITEMS = 10

DELETE_OUTPUT_DIRECTORY = False
DISQUS_SITENAME = "toledano"
GOOGLE_ANALYTICS = "UA-130534-3"
