# -*- coding: utf-8 -*-


DATABASES = {
    'default': {
        # Replace 'sqlite3' with 'postgresql_psycopg2' or 'mysql'.
        'ENGINE': 'django.db.backends.mysql',
        # Database name or path to database file if using sqlite3.
        'NAME': 'bu_pootle',
        # Not used with sqlite3.
        'USER': '…',
        # Not used with sqlite3.
        'PASSWORD': '…',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
        # See https://docs.djangoproject.com/en/1.6/topics/db/transactions/
        # required for Django 1.6 + sqlite
        'ATOMIC_REQUESTS': True,
    }
}