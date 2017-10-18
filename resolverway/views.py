#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import inspect

from flask import request, Blueprint, Response, redirect, render_template
from flask_discoverer import advertise
from flask import Response
import requests

from adsmutils import load_config, setup_logging

import resolverway
from resolverway.log import log_request

bp = Blueprint('resolver_gateway', __name__)

class LinkRequest():

    bibcode = ''
    link_type = ''
    link_sub_type = ''
    username = ''

    logger = None
    config = {}

    def __init__(self, bibcode, link_type, url):
        self.config = {}
        self.config.update(load_config(proj_home=os.path.dirname(inspect.getsourcefile(resolverway))))

        self.logger = setup_logging('resolver_service', self.config.get('LOG_LEVEL', 'INFO'))

        self.bibcode = bibcode
        self.link_type = link_type
        self.url = url


    def __return_response_error(self, response, status):
        self.logger.info('sending response status={status}'.format(status=status))
        self.logger.debug('sending response text={response}'.format(response=response))

        r = Response(response=response, status=status)
        r.headers['content-type'] = 'text/plain; charset=UTF-8'
        return r


    def __log_request_info(self):
        self.logger.info('received request with bibcode={bibcode} and link_type={link_type}'.format(
            bibcode=self.bibcode, link_type=self.link_type))
        if self.username:
            self.logger.info('and username={username}'.format(username=self.username))
        if self.referrer:
            self.logger.info('also referrer={referrer}'.format(referrer=self.referrer))


    def process_request(self):
        """

        :return:
        """
        self.username = request.cookies.get('username', '')
        self.referrer = request.referrer

        self.__log_request_info()

        # if there is a url we need to log the request and redirect
        if (self.url != None):
            log_request(self.bibcode, self.username, self.link_type, self.url, self.referrer)
            self.logger.debug('redirecting to {url}'.format(url=self.url))
            return redirect(self.url, 302)

        params = self.bibcode + '/' + self.link_type
        response = requests.get(url=self.config['RESOLVER_SERVICE_URL'].format(params), headers=request.headers)

        contentType = response.headers.get('content-type')

        if (contentType == 'text/plain; charset=UTF-8'):
            self.logger.info('redirecting to {url}'.format(url=response.text))
            return redirect(response.text, 302)
        elif (contentType == 'application/json'):
            links = response.json()['links']['records']
            if links:
                log_request(self.bibcode, self.username, self.link_type, self.url, self.referrer)
                self.logger.debug('rendering template with data {links}'.format(links=links))
                return render_template('list.html', link_type=self.link_type.title(),
                    links=links, bibcode=self.bibcode)

        return self.__return_response_error(response='', status=404)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/resolver/<bibcode>/<link_type>', defaults={'url': None}, methods=['GET'])
@bp.route('/resolver/<bibcode>/<link_type>/<path:url>', methods=['GET'])
def resolver(bibcode, link_type, url):
    return LinkRequest(bibcode, link_type.upper(), url).process_request()



