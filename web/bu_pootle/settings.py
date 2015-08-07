#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sample configuration file.

This file includes the settings that administrators will likely change.
You can find the defaults in the ``*.conf`` files for more advanced settings.

In order for this configuration changes to take effect, bear in mind that you
need to change the extension of this file from ``.conf.sample`` to ``.conf``.
"""

import os

try:
    _settings_file_path = pootle_settings_filepath
except NameError:
    _settings_file_path = __file__
MODULE_ROOT = os.path.dirname(os.path.abspath(_settings_file_path))
PROJECT_ROOT = os.path.dirname(MODULE_ROOT)


#
# Base
#

# Site title
POOTLE_TITLE = 'BU Translation Server'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'PzZy2k4lBZAFsWF1J2QpyRTvqrzJuj0/96EaW8SO4DNANfZ4hOOH6Vrj8xbs0v0Ygf0='

# A list of strings representing the host/domain names that this Pootle server
# can serve. This is a Django's security measure. More details at
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = [
#     '127.0.0.1',
#     'localhost',
#     #'${your_server}',
# ]


#
# Backends
#

# Database backend settings
DATABASES = {
    'default': {
        # Replace 'sqlite3' with 'postgresql_psycopg2' or 'mysql'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Database name or path to database file if using sqlite3.
        'NAME': os.path.join(PROJECT_ROOT, 'pootle.db'),
        # Not used with sqlite3.
        'USER': '',
        # Not used with sqlite3.
        'PASSWORD': '',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
        # See https://docs.djangoproject.com/en/1.6/topics/db/transactions/
        # required for Django 1.6 + sqlite
        'ATOMIC_REQUESTS': True,
    }
}


# Cache Backend settings

# For more information, check
# http://docs.djangoproject.com/en/dev/topics/cache/#setting-up-the-cache
# and http://niwibe.github.io/django-redis/
CACHES = {
   'default': {
       'BACKEND': 'django_redis.cache.RedisCache',
       'LOCATION': 'redis://127.0.0.1:6379/1',
       'TIMEOUT': 60,
   },
   'redis': {
       'BACKEND': 'django_redis.cache.RedisCache',
       'LOCATION': 'redis://127.0.0.1:6379/2',
       'TIMEOUT': None,
   },
   'stats': {
       'BACKEND': 'django_redis.cache.RedisCache',
       'LOCATION': 'redis://127.0.0.1:6379/3',
       'TIMEOUT': None,
   },
   'exports': {
       'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
       'LOCATION': os.path.join(PROJECT_ROOT, 'exports/'),
       'TIMEOUT': 259200,  # 3 days.
   },
}

#
# Logging
#

# The directory where Pootle writes its logs
POOTLE_LOG_DIRECTORY = os.path.join(PROJECT_ROOT, 'log')


#
# Site
#

# This Pootle server admins
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

# Mail settings

# Default email address to use for messages sent by Pootle.
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = 'info@browser-update.org'

# Address to receive messages sent by contact form.
POOTLE_CONTACT_EMAIL = 'info@browser-update.org'
POOTLE_CONTACT_ENABLED = True

# Email address to report string errors to, unless a report email was set for
# the project for which the string error is being reported.
# Use this as a way to forward string error reports to an address
# different from the general contact address.
POOTLE_CONTACT_REPORT_EMAIL = 'info@browser-update.org'

# Mail server settings

# By default Pootle uses the SMTP server on localhost. If the server is not
# configured for sending emails, uncomment and use these settings to setup an
# external outgoing SMTP server.

# Example for Google as an external SMTP server
#EMAIL_HOST_USER = 'USER@YOUR_DOMAIN.com'
#EMAIL_HOST_PASSWORD = 'YOUR_PASSWORD'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True


#
# Translation
#

# The directory where the translation files are kept
POOTLE_TRANSLATION_DIRECTORY = os.path.join(PROJECT_ROOT, 'translations')

# Two-tuple defining the markup filter to apply in certain textareas.
#
# - Accepted values for the first element are 'textile', 'markdown',
#   'restructuredtext' and None.
# - The second element should be a dictionary of keyword arguments that will be
#   passed to the markup function.
#
# IMPORTANT: If you want to use one of these markup filters you must install on
# your own the required packages.
#
# Examples:
#    POOTLE_MARKUP_FILTER = (None, {})
#    POOTLE_MARKUP_FILTER = ('markdown', {'safe_mode': 'escape'})
#    POOTLE_MARKUP_FILTER = ('restructuredtext', {
#                                'settings_overrides': {
#                                    'report_level': 'quiet',
#                                }
#                            })
POOTLE_MARKUP_FILTER = (None, {})

# Set the backends you want to use to enable translation suggestions through
# several online services. To disable this feature completely just comment all
# the lines to set an empty list [] to the POOTLE_MT_BACKENDS setting.
#
# The second parameter for each backend option is the API key, which will
# be used in case the service supports using an API key.
#
# Available options are:
# 'APERTIUM': Apertium service.
#             For this service you need to set the API key.
#             Get your key at http://api.apertium.org/register.jsp
# 'GOOGLE_TRANSLATE': Google Translate service.
#             For this service you need to set the API key.
#             Note that Google Translate API is a paid service
#             See more at https://cloud.google.com/translate/v2/pricing
#
POOTLE_MT_BACKENDS = [
#        ('APERTIUM', ''),
#        ('GOOGLE_TRANSLATE', ''),
#        ('YANDEX_TRANSLATE', ''),
]

# Behind proxy / deployment
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_HTTPS', 'on')
ALLOWED_HOSTS = ('*',)  # Apache will take care of validation

_local_settings_path = os.path.join(MODULE_ROOT, 'local_settings.py')
if os.path.exists(_local_settings_path):
    execfile(_local_settings_path)
