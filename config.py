#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

# In what environment are we?
ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging').lower()
# Configure logging
RESOLVER_GATEWAY_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'formatter': 'default',
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/tmp/resolver_service_app.{}.log'.format(ENVIRONMENT),
        },
        'console': {
            'formatter': 'default',
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file','console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# This is the URL to communicate with resolver_service api
RESOLVER_SERVICE_URL = 'http://localhost:4000/v1/resolver/{}'

ADSWS_API_TOKEN = 'Bearer:eQhhOLITyCD1B2Afuxf2b5LdTpFTl5WaepVI7Dn0'