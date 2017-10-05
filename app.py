#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, Blueprint, Response, redirect, render_template
from flask_discoverer import advertise
import requests

from adsputils import load_config, setup_logging

from logRequest import *

app = Flask(__name__)

logger = None
config = {}

@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@app.route('/resolver/<bibcode>/<linkType>', defaults={'url': None}, methods=['GET'])
@app.route('/resolver/<bibcode>/<linkType>/<path:url>', methods=['GET'])
def resolver(bibcode, linkType, url):

    global logger
    global config

    if logger == None:
        config.update(load_config())
        logger = setup_logging('resolver_service', config.get('LOG_LEVEL', 'INFO'))

    userName = request.cookies.get('username', '')
    referrer = request.referrer

    logger.info('received request with bibcode={bibcode} and linkType={linkType} with username={userName} and referrer={referrer}'
                .format(bibcode=bibcode, linkType=linkType, userName=userName, referrer=referrer))

    # if there is a url we need to log the request and redirect
    if (url != None):
        logger.info('redirecting to {url}'.format(url=url))
        return redirect(url, 302)

    params = bibcode + '/' + linkType
    response = requests.get(url=config['RESOLVER_SERVICE_URL'].format(params), headers=request.headers)

    contentType = response.headers.get('content-type')

    if (contentType == 'text/html; charset=UTF-8'):
        logger.info('redirecting to {url}'.format(url=response.text))
        return redirect(response.text, 302)
    elif (contentType == 'application/json'):
        logger.info('rendering page')
        links = response.json()['links']['records']
        responseText = render_template(
            'list.html',
            linkType=linkType.title(),
            links=links,
            bibcode=bibcode)
        return returnResponse(bibcode=bibcode, userName=userName, linkType=linkType, url='',
                              referrer=referrer, response=responseText, status=200)
    else:
        return returnResponseError(response='', status=404)


def returnResponse(bibcode, userName, linkType, url, referrer, response, status):
    logger.info('sending response status={status}'.format(status=status))
    logger.debug('sending response text={response}'.format(response=response))

    if (len(response) != 0):
        sendLog(bibcode, userName, linkType, url, referrer)
        r = Response(response=response, status=status)
        r.headers['content-type'] = 'text/html; charset=UTF-8'
        return r
    returnResponseError(response, status)


def returnResponseError(response, status):
    logger.info('sending response status={status}'.format(status=status))
    logger.debug('sending response text={response}'.format(response=response))

    r = Response(response=response, status=status)
    r.headers['content-type'] = 'text/html; charset=UTF-8'
    return r


if __name__ == "__main__":
    app.run(debug=True)