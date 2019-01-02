#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Javier Sanchez Toledano'
SITENAME = u'Yo, Toledano'
SITEURL = ''
STATICURL = 'https://media.toledano.org'
SITELOGO = 'https://media.toledano.org/images/toledano-4.png'
TAGLINE = 'Oh tiempo tus piramides'
TAG_LINE = TAGLINE
DEFAULT_METADATA = {
    'about_author': '''Soy programador en Django+Python y WordPress.
        Auditor líder certificado en la norma ISO 9001:2008.
        Fotógrafo aficionado.''',
    'email': 'js.toledano@me.com',
    'author': 'Javier Sanchez Toledano'
}
PROFILE_IMAGE_URL = 'https://media.toledano.org/images/yo.jpg'
COVER_IMG = 'https://media.toledano.org/images/category_add.jpg'
# COVER_IMG = 'https://media.toledano.org/fototeca/portada2-compressed.jpg'
ARTICLE_COVER = 'https://media.toledano.org/images/article_cover.png'
DOMAIN = "yo.toledano.org"
FEEDBURNER = "//feeds.feedburner.com/toledano/rss"

# ################ CASPER
AUTHOR_PIC_URL = PROFILE_IMAGE_URL
AUTHOR_BIO = DEFAULT_METADATA['about_author']
AUTHOR_LOCATION = 'Tlaxcala, México'
SITE_DESCRIPTION = TAGLINE
SITE_LOGO = SITELOGO
DEFAULT_HEADER_IMAGE = COVER_IMG
ARCHIVE_HEADER_IMAGE = ARTICLE_COVER
VECINO_ANTERIOR = 'https://media.toledano.org/images/01-anterior.jpg'
VECINO_SIGUIENTE = 'https://media.toledano.org/images/01-nuevo.jpg'
# ./CASPER


ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = '{category}/{slug}.html'
CATEGORY_URL = '{slug}/index.html'
CATEGORY_SAVE_AS = '{slug}/index.html'
TAGS_SAVE_AS = 'tag/index.html'
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

PATH = 'content'

# Metadata (partials/_metaheader.html)
PUBLISHER = ''
GOOGLE_SV = 'hiMLLh1Fgb1J0rpXE4fw3zc7rRzKzbsg0y3c-6gujw0'
ALEXA = ''
MY_WOT = ''
MSVALIDATE = ''
GOOGLE_ANALYTICS = 'UA-130534-3'

# OpenGraph
USE_OPEN_GRAPH = True
TWITTER_USERNAME = "jstoledano"
SITE_LANG = "es_MX"
SITE_LANG_ALTERNATE = "es"
DISQUS_SITENAME = "toledano"
OPEN_GRAPH_FB_APP_ID = "112184015464389"

TIMEZONE = 'Mexico/General'
DEFAULT_LANG = u'es'
LOCALE = 'es_ES.UTF-8'
DEFAULT_DATE_FORMAT = '%A, %d de %B de %Y'

PLUGIN_PATHS = ['../pelican-plugins', ]
PLUGINS = ['tag_cloud', 'neighbors', 'series', 'sitemap']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {},
        'markdown.extensions.extra': {},
        'markdown.extensions.admonition': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.smarty': {},
        'markdown.extensions.toc': {},
        'markdown.extensions.sane_lists': {}
    }
}

PYGMENTS_RST_OPTIONS = {'cssclass': 'codehilite', }

TAG_CLOUD_STEPS = 5

THEME = 'themes/casper'

CATS = {
  'audioteca': ['Audioteca Toledana', 'La mejor selección de la música mundial', 'music'],
  'fototeca': ['Fototeca Toledana', 'Conoce el mundo, visto desde un enfoque único', 'camera-retro'],
  'desarrollo': ['Desarrollo Web', 'Notas sobre desarrollo con Python, Django, JavaScript y mucho más', 'code'],
  'calidad': ['Calidad', 'Artículos sobre la implementación de la Norma ISO 9001', 'certificate'],
  'opinion': ['Opinión', 'Artículos de opinión personal', 'coffee'],
  'trinos': ['Céfiros y Trinos', 'Notas rápidas que encuentro navegando en Internet', 'retweet']
}

TYPOGRIFY = True

SOCIAL = (
    ('github-square', 'https://github.com/jstoledano/'),
    ('twitter-square', 'https://twitter.com/jstoledano'),
    ('facebook-square', 'https://facebook.com/yo.toledano')
)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 5

CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/BingSiteAuth.xml': {'path': 'BingSiteAuth.xml'},
    'extra/keybase.txt': {'path': 'keybase.txt'}
}

SITEMAP = {
    'exclude': ['tag/', 'category/'],
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
