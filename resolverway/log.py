#!/usr/bin/python
# -*- coding: utf-8 -*-

import watchtower, logging
import datetime
import os

loggers = {}

def log_request(bibcode, user, link_type, url, referrer):
    """
    log to aws
    :param bibcode: 
    :param user: 
    :param link_type: 
    :param url: 
    :param referrer: 
    """
    global loggers
    global server, host
    logger = logging.getLogger(__name__)
    if not len(logger.handlers):
        logging.basicConfig(level=logging.INFO)
        server = str(os.uname()[1])
        host = str(os.getpid())
        handler = watchtower.CloudWatchLogHandler(stream_name=server + "-" + host + "-app",
                                                  log_group="production-resolver-app")
        logger.addHandler(handler)

    logger.info('"{dateUTC}" "{server}" "{host}" "{user}" "{link}" "{bibcode}" "{service}" "{referer}"'.format(
        dateUTC=datetime.datetime.utcnow().isoformat(),
        server=server,
        host=host,
        user=user,
        link=link_type,
        bibcode=bibcode,
        service=url,
        referer=referrer))

