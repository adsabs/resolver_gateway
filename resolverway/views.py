
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
    user_id = None
    referrer = None

    def __init__(self, bibcode, link_type, url):
        self.bibcode = bibcode
        self.link_type = link_type
        self.url = url
        self.link_sub_type = ''
        self.username = None
        self.user_id = None
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
                current_app.logger.info('redirecting to %s' %(link))
                log_request(self.bibcode, self.username, self.user_id, self.link_type, link, self.referrer, self.client_id, self.access_token)
                return self.redirect(link)

        # when action is to display, there are more than one link, so render template to display links
        if (action == 'display'):
            links = the_json_response.get('links', None)
            if links:
                records = links.get('records', None)
                if records:
                    current_app.logger.debug('rendering template with data %s' %(records))
                    log_request(self.bibcode, self.username, self.user_id, self.link_type, self.url, self.referrer, self.client_id, self.access_token)
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
            self.referrer = request.referrer
            session = request.cookies.get('session', None)
            if session:
                # Translate session stored in the cookie into user account details
                redis = current_app.extensions['redis']
                try:
                    account = redis[session] # is it in the cache already?
                except KeyError:
                    account = None
                if account is None:
                    try:
                        r = requests.get(url=current_app.config['ACCOUNT_TOKEN_SERVICE_URL'], cookies=request.cookies)
                        if r.status_code == 200:
                            account = r.json()
                            redis[session] = account # Cache response
                    except HTTPError as e:
                        current_app.logger.error("Http Error: %s" %(e))
                    except ConnectionError as e:
                        current_app.logger.error("Error Connecting: %s" %(e))
                if account:
                    self.username = account['username']
                    self.user_id = account['user_id']
                    self.client_id = account['client_id']
                    self.access_token = account['access_token']

        # log the request
        current_app.logger.info('received request with bibcode=%s and link_type=%s' %(self.bibcode, self.link_type))
        if self.username or self.user_id or self.client_id or self.access_token:
            current_app.logger.info('and username=%s, user_id=%s, client_id=%s, access_token=%s' %(self.username, self.user_id, self.client_id, self.access_token))
        if self.referrer:
            current_app.logger.info('also referrer=%s' %(self.referrer))

        # if there is a url we need to log the request and redirect
        if (self.url != None):
            current_app.logger.debug('received to redirect to %s' %(self.url))
            log_request(self.bibcode, self.username, self.user_id, self.link_type, self.url, self.referrer, self.client_id, self.access_token)
            return self.redirect(self.url)

        try:
            # if no url then send request to resolver_service to get link(s)
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
@bp.route('/resolver/<bibcode>', defaults={'link_type': '', 'url': None}, methods=['GET'])
@bp.route('/resolver/<bibcode>/<link_type>', defaults={'url': None}, methods=['GET'])
@bp.route('/resolver/<bibcode>/<link_type>/<path:url>', methods=['GET'])
def resolver(bibcode, link_type, url):
    """

    :param bibcode:
    :param link_type:
    :param url:
    :return:
    """
    return LinkRequest(bibcode, link_type.upper(), url).process_request()



