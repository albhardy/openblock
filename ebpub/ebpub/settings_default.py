#   Copyright 2007,2008,2009,2011 Everyblock LLC, OpenPlans, and contributors
#
#   This file is part of ebpub
#
#   ebpub is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   ebpub is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with ebpub.  If not, see <http://www.gnu.org/licenses/>.
#

"""
This file should rarely need editing; if it does, you might want to
move the setting in question into settings.py (and settings.py.in)

Known required settings are: %r
"""

import os
import imp

EBPUB_DIR = imp.find_module('ebpub')[1]
DJANGO_DIR = imp.find_module('django')[1]


########################
# CORE DJANGO SETTINGS #
########################

required_settings=[
    'DEBUG',
    # Database configuration as per
    # http://docs.djangoproject.com/en/1.2/topics/db/multi-db/
    # There's an example in obdemo/settings.py.in
    'DATABASES',
]

TEMPLATE_DIRS = (
    os.path.join(EBPUB_DIR, 'templates'),
    os.path.join(DJANGO_DIR, 'contrib', 'gis', 'templates'),
    # django template override hack to partially override templates
    # by referring to them with a unique path, see:
    # http://stackoverflow.com/questions/3967801/django-overriding-and-extending-an-app-template
    # You can use {% extends "ebpub/templates/..." %} to partially extend a template
    os.path.dirname(EBPUB_DIR)
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'ebpub.accounts.context_processors.user',
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'ebpub.db.context_processors.map_context',
    'ebpub.db.context_processors.settings_context',
    'django.core.context_processors.request',
    #'django.core.context_processors.debug',
)

AUTHENTICATION_BACKENDS = (
    'ebpub.accounts.models.AuthBackend',
)

INSTALLED_APPS = (
    'background_task',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_static',
    'ebdata.blobs',
    'ebdata.geotagger',
    'ebpub.accounts',
    'ebpub.alerts',
    'ebpub.db',
    'ebpub.geocoder',
    'ebpub.moderation',
    'ebpub.neighbornews',
    'ebpub.openblockapi',
    'ebpub.openblockapi.apikey',
    'ebpub.petitions',
    'ebpub.preferences',
    'ebpub.richmaps',
    'ebpub.savedplaces',
    'ebpub.streets',
    'ebpub.widgets',
    'obadmin.admin',
    'olwidget',
    'easy_thumbnails',
)

APPS_FOR_TESTING = (
    # Don't need these installed at runtime, but I've put them here so
    # manage.py test can automatically find their tests.
    'ebdata.nlp',
    'ebdata.templatemaker',
    'ebdata.textmining',
    'ebpub.metros',
    'ebpub.utils',
    'ebpub.geocoder',
    'ebpub.geocoder.parser',
)

APPS_NOT_FOR_TESTING = (
        # the user model used is custom.
        'django.contrib.auth',
        # this makes too many weird assumptions about the database underpinnings
        'django.contrib.contenttypes',
        # these tests break with some settings, see https://github.com/peterbe/django-static/issues#issue/8 and 9
        'django_static',
        # these tests break under django 1.3, unsure why.
        'django.contrib.messages',
        # the rest are just not of interest.
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.gis',
        'olwidget',
        'olwidget.models',
        'south',
        'background_task',
        'easy_thumbnails',
)


INSTALLED_APPS = INSTALLED_APPS + APPS_FOR_TESTING + ('south',)

TEST_RUNNER = 'obadmin.testrunner.TestSuiteRunner'

# Messages backend. OpenBlock doesn't use it (yet) but this silences a
# deprecationwarning from the admin UI in django 1.3.
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'


# South - database migration config
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = True

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'ebpub.accounts.middleware.UserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

SITE_ID = 1

# Limit size of uploads, then fall back to standard upload behavior.
FILE_UPLOAD_HANDLERS = (
    "ebpub.utils.uploadhandler.QuotaUploadHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    )

LOGIN_URL = '/accounts/login/'

##################################
# CUSTOM OPENBLOCK SETTINGS      #
##################################

# Which LocationType to show when you visit /locations
DEFAULT_LOCTYPE_SLUG = 'neighborhoods'
required_settings.append('DEFAULT_LOCTYPE_SLUG')

# This may be needed to get tests to build.
POSTGIS_TEMPLATE = 'template_postgis'

# The domain for your site.
required_settings.append('EB_DOMAIN')

# This is the short name for your city, e.g. "chicago".
required_settings.append('SHORT_NAME')

# Set both of these to distinct, secret strings that include two instances
# of '%s' each. Example: 'j8#%s%s' -- but don't use that, because it's not
# secret.
required_settings.extend(['PASSWORD_CREATE_SALT', 'PASSWORD_RESET_SALT'])

# The list of all metros this installation covers. This is a tuple of
# dictionaries.  If your site only covers one city, there will be
# only one dictionary.
# There's an example in obdemo/settings.py.in
required_settings.append('METRO_LIST')

# How many days of news to show on many views.
required_settings.append('DEFAULT_DAYS')

# Overrides datetime.datetime.today(), for development.
EB_TODAY_OVERRIDE = None

# Filesystem location of scraper log.
required_settings.append('SCRAPER_LOGFILE_NAME')

# Do you want scrapers to email you errors directly?
# (Used by the framework in ebdata/ebdata/retrieval/scrapers/)
# We default to false, because we typically have Cron send email on errors.
required_settings.append('SCRAPER_LOG_DO_EMAIL_ERRORS')
SCRAPER_LOG_DO_EMAIL_ERRORS = False

# Edit this if you want to control where
# scraper scripts will put their HTTP cache.
# (Warning, don't put it in a directory encrypted with ecryptfs
# or you'll likely have "File name too long" errors.)
HTTP_CACHE = '/tmp/openblock_scraper_cache'

# If this cookie is set with the given value, then the site will give the user
# staff privileges (including the ability to view non-public schemas).
required_settings.extend(['STAFF_COOKIE_NAME', 'STAFF_COOKIE_VALUE'])


# SCHEMA_MANAGER_HOOK: Set this to a string like
# 'package_name.module_name:function_name'
# This is an advanced feature that can be used to modify all Schema
# queries based on the current request.  The named function should
# take arguments (request, manager) and return either a Manager or
# something that looks like one - maybe by proxying it - for example
# by doing extra filtering in get_query_set().
SCHEMA_MANAGER_HOOK = None


######################################################
#  EMAIL                                             #
######################################################

# This is used as a "From:" in e-mails sent to users.
required_settings.append('GENERIC_EMAIL_SENDER')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='localhost'
EMAIL_PORT='25'
# Need authentication to send mail? Set these.
#EMAIL_HOST_USER=''
#EMAIL_HOST_PASSWORD=''
#EMAIL_USE_TLS=False  # For secure SMTP connections.


##############################################
# OPENBLOCK MAP CONFIGURATION                #
##############################################

# Where to center citywide maps by default.
required_settings.append('DEFAULT_MAP_CENTER_LON')
required_settings.append('DEFAULT_MAP_CENTER_LAT')
required_settings.append('DEFAULT_MAP_ZOOM')

# Which base layer to use on maps.
# May be any of the default olwidget base layers,
# as per http://olwidget.org/olwidget/v0.4/doc/olwidget.js.html#general-map-display
# or you may use 'custom.X' where X is a key in MAP_CUSTOM_BASE_LAYERS, see below.

# For example:
#MAP_BASELAYER_TYPE = 'google.streets'
MAP_BASELAYER_TYPE = 'custom.opengeo_osm'
required_settings.append('MAP_BASELAYER_TYPE')


# If you set MAP_BASELAYER_TYPE='google.*', you must also set GOOGLE_API_KEY.
GOOGLE_API_KEY=''

# Use a specific version of google maps API to work around
# copyright alert bug:
# http://trac.osgeo.org/openlayers/ticket/2984
GOOGLE_API='http://maps.google.com/maps/api/js?v=3.6&sensor=false'

# If you set MAP_BASELAYER_TYPE='yahoo', you must also set YAHOO_APP_ID.
YAHOO_APP_ID=''
# If you want MAP_BASELAYER_TYPE='cloudmade.*', you must also set CLOUDMADE_API_KEY.
CLOUDMADE_API_KEY=''

# You can use ANY OpenLayers base layer configuration, with a little extra work,
# like so:
MAP_CUSTOM_BASE_LAYERS = {
    'opengeo_osm':  # to use this, set MAP_BASELAYER_TYPE='custom.opengeo_osm'
        {"class": "WMS",  # The OpenLayers.Layer subclass to use.
         "args": [  # These are passed as arguments to the constructor.
            "OpenStreetMap (OpenGeo)",
            "http://maps.opengeo.org/geowebcache/service/wms",
            {"layers": "openstreetmap",
             "format": "image/png",
             "bgcolor": "#A1BDC4",
             },
            {"wrapDateLine": True
             },
            ],
         }
}

##########################
#  MEDIA                 #
##########################

# Core Django settings for static media and uploaded files,
# see https://docs.djangoproject.com/en/dev/ref/settings/#media-root

# Where static media live.
STATIC_ROOT = os.path.join(EBPUB_DIR, 'media')
# Where to serve these files.  For production deployment, ensure your
# webserver makes STATIC_ROOT available at this URL.
STATIC_URL = '/'

# Where to put files uploaded by users.
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'uploads')
# Where to serve these files.  For production deployment, ensure your
# webserver makes MEDIA_ROOT available at this URL.
MEDIA_URL = '/uploads/'

required_settings.extend(['STATIC_ROOT', 'MEDIA_ROOT', 'STATIC_URL', 'MEDIA_URL'])


# Static media optimizations: whitespace slimming, URL timestamping.
# see https://github.com/peterbe/django-static#readme
# This supercedes the old everyblock-specific template tags in
# everyblock.templatetags.staticmedia.
DJANGO_STATIC = True
DJANGO_STATIC_MEDIA_ROOTS = [MEDIA_ROOT, STATIC_ROOT,]


# Putting django-static's output in a separate directory and URL space
# makes it easier for git to ignore them,
# and easier to have eg. apache set appropriate expiration dates.
DJANGO_STATIC_NAME_PREFIX = '/cache-forever'
# Make sure you have write permission here!!
DJANGO_STATIC_SAVE_PREFIX = os.path.join(STATIC_ROOT, DJANGO_STATIC_NAME_PREFIX[1:])


#############################
# JAVASCRIPT LIBRARIES      #
#############################


# For local development you might try this:
#JQUERY_URL = '/media/js/jquery.js'
JQUERY_URL = 'http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js'

# It's important that it be named exactly OpenLayers.js,
# see http://trac.osgeo.org/openlayers/ticket/2982
OPENLAYERS_URL = '/scripts/OpenLayers-2.11/OpenLayers.js'
OPENLAYERS_IMG_PATH = '/scripts/OpenLayers-2.11/img/'

# For compatibility with django-olwidget
OL_API = OPENLAYERS_URL



########################################
#  OPENBLOCK REST API                  #
########################################

MAX_KEYS_PER_USER=1

API_THROTTLE_AT=150  # max requests per timeframe.
API_THROTTLE_TIMEFRAME = 60 * 60 # default 1 hour.
# How long to retain the times the user has accessed the API. Default 1 week.
API_THROTTLE_EXPIRATION = 60 * 60 * 24 * 7

# NOTE in order to enable throttling, you MUST also configure
# CACHES['default'] to something other than a DummyCache.  See the CACHES
# setting.


#########################################
# CACHING                               #
#########################################

## For development & testing, DummyCache makes for easiest troubleshooting.
## See https://docs.djangoproject.com/en/1.3/ref/settings/#std:setting-CACHES
#
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    # File caching might be a reasonable choice for low-budget, memory-constrained
    # hosting environments.
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     'LOCATION': 'file:///tmp/myblock_cache',
    # }
}

###############################################
# API KEYS for third-party services           #
###############################################

# Neighbornews app opptionally uses ReCaptcha.
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''


################################################
#  OTHER                                       #
################################################

# Set this True to cache geocoder results in the database;
# it's faster but makes troubleshooting harder.
# (Why doesn't it just use the normal django caching framework?)
EBPUB_CACHE_GEOCODER = True
required_settings.append('EBPUB_CACHE_GEOCODER')

# Required by openblockapi.apikey to associate keys with user profiles.
AUTH_PROFILE_MODULE = 'preferences.Profile'

# ebpub.neighbornews optionally uses recaptcha.  This can be True,
# False, or a string representing a path in the form
# 'packagename.modulename:functionname' path to a function that takes
# a request argument and returns True or False.
NEIGHBORNEWS_USE_CAPTCHA = False

# Batch jobs (django-background-task): how long (in seconds) can a job
# be locked before we decide it's dead?
MAX_RUN_TIME = 60 * 15
# How many failures to retry?
MAX_ATTEMPTS = 4

# Maximum size of user-uploaded images, relevant to eg. the
# NeighborNews schemas.
UPLOAD_MAX_MB = 10.0

########################################################
# LOGGING                                              #
########################################################

# See https://docs.djangoproject.com/en/dev/topics/logging
# We import this first because South annoyingly overrides its log level at import time.
from south import logger as _unused

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(module)s: %(message)s'
            },
        'debug': {
            'format': '%(levelname)s %(asctime)s P: (process)d T: %(thread)d in %(module)s:%(pathname)s:%(lineno)d %(message)s'
            },
        'verbose': {
            'format': '%(levelname)s %(asctime)s P: (process)d T: %(thread)d in %(module)s: %(message)s'
            },
    },
    'handlers': {
        'null': {
            'level':'INFO',
            'class':'django.utils.log.NullHandler',
            },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
            },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose'
            },
        },
    'loggers': {
        '': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
            },
        'django': {
            'handlers': [],
            'propagate': True,
            'level':'WARN',
            },
        'ebpub': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
            },
        'ebdata': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
            },
        # 'django.request': {
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
        'south': {
            'handlers': [],
            'level': 'INFO',
        }
    }
}


__doc__ = __doc__ % required_settings
