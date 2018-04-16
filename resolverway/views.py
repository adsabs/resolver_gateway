
from flask import current_app, request, Blueprint, Response, redirect, render_template
from flask_discoverer import advertise
from flask import Response
import requests
from requests.exceptions import HTTPError, ConnectionError

from resolverway.log import log_request

bp = Blueprint('resolver_gateway', __name__)

class LinkRequest():

    bibcode = ''
    link_type = ''
    link_sub_type = ''
    url = None
    username = None
    referrer = None

    def __init__(self, bibcode, link_type, url=None, id=None):
        self.bibcode = bibcode
        self.link_type = link_type
        self.url = url
        self.id = id
        self.link_sub_type = ''
        self.username = None
        self.client_id = None
        self.access_token = None
        self.referrer = None

    def redirect(self, link):
        response = redirect(link, 302)
        response.autocorrect_location_header = False
        return response, 302

    def process_resolver_response(self, the_json_response):
        action = the_json_response.get('action', '')

        # when action is to redirect, there is only one link, so redirect to link
        if (action == 'redirect'):
            link = the_json_response.get('link', None)
            if link:
                # gunicorn does not like / so it is passed as underscore and returned back to / here
                if self.link_type == 'DOI':
                    link = link.replace(',', '/')

                current_app.logger.info('redirecting to %s' %(link))
                log_request(self.bibcode, self.username, self.link_type, link, self.referrer, self.client_id, self.access_token)
                return self.redirect(link)

        # when action is to display, there are more than one link, so render template to display links
        if (action == 'display'):
            links = the_json_response.get('links', None)
            if links:
                records = links.get('records', None)
                if records:
                    current_app.logger.debug('rendering template with data %s' %(records))
                    log_request(self.bibcode, self.username, self.link_type, self.url, self.referrer, self.client_id, self.access_token)
                    return render_template('list.html', url="", link_type=self.link_type.title(),
                        links=records, bibcode=self.bibcode), 200

        # if we get here there is an error, so display error template
        current_app.logger.debug('The requested resource does not exist.')
        return render_template('400.html'), 400

    def process_request(self):
        """

        :return:
        """
        if request:
            self.username = request.cookies.get('username', None)
            self.client_id = request.cookies.get('client_id', None)
            self.access_token = request.cookies.get('access_token', None)
            self.referrer = request.referrer

        # log the request
        current_app.logger.info('received request with bibcode=%s and link_type=%s' %(self.bibcode, self.link_type))
        if self.username or self.client_id or self.access_token:
            current_app.logger.info('and username=%s, client_id=%s, access_token=%s' %(self.username, self.client_id, self.access_token))
        if self.referrer:
            current_app.logger.info('also referrer=%s' %(self.referrer))

        # if there is a url we need to log the request and redirect
        if (self.url != None):
            current_app.logger.debug('received to redirect to %s' %(self.url))
            log_request(self.bibcode, self.username, self.link_type, self.url, self.referrer, self.client_id, self.access_token)
            return self.redirect(self.url)

        try:
            # if no url then send request to resolver_service to get link(s)
            if (self.id != None):
                params = self.bibcode + '/' + self.link_type + ':' + self.id
            else:
                params = self.bibcode + '/' + self.link_type
            headers = {'Authorization': 'Bearer ' + current_app.config['RESOLVER_SERVICE_ADSWS_API_TOKEN']}
            response = requests.get(url=current_app.config['RESOLVER_SERVICE_URL'] %(params), headers=headers)
    
            contentType = response.headers.get('content-type')
    
            # need to make sure the response is json
            if (contentType == 'application/json'):
                return self.process_resolver_response(response.json())
        except HTTPError as e:
            current_app.logger.error("Http Error: %s" %(e))
        except ConnectionError as e:
            current_app.logger.error("Error Connecting: %s" %(e))
            
        return render_template('400.html'), 400


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/link_gateway/<bibcode>', defaults={'link_type': '', 'url': None}, methods=['GET'])
@bp.route('/link_gateway/<bibcode>/<link_type>', defaults={'url': None}, methods=['GET'])
@bp.route('/link_gateway/<bibcode>/<link_type>/<path:url>', methods=['GET'])
def resolver(bibcode, link_type, url):
    """

    :param bibcode:
    :param link_type:
    :param url:
    :return:
    """
    return LinkRequest(bibcode, link_type.upper(), url=url).process_request()


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/link_gateway/<bibcode>/<link_type>:<path:id>', methods=['GET'])
def resolver_id(bibcode, link_type, id):
    """
    endpoint for identification link types: doi and arXiv
    :param bibcode:
    :param link_type:
    :param id:
    :return:
    """
    return LinkRequest(bibcode, link_type.upper(), id=id).process_request()


