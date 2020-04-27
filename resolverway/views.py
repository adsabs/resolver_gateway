
from flask import current_app, request, Blueprint, Response, redirect, render_template
from flask_redis import FlaskRedis
from redis import RedisError
from flask_discoverer import advertise
from requests.exceptions import HTTPError, ConnectionError
import ast
import urllib
import urlparse

from resolverway.log import log_request

bp = Blueprint('resolver_gateway', __name__)
redis_db = FlaskRedis()


class LinkRequest():

    bibcode = ''
    link_type = ''
    link_sub_type = ''
    url = None
    user_id = None
    referrer = None

    def __init__(self, bibcode, link_type, url=None, id=None):
        self.bibcode = bibcode
        self.link_type = link_type
        self.url = url
        self.id = id
        self.link_sub_type = ''
        self.user_id = None
        self.client_id = None
        self.referrer = None
        self.user_agent = None
        self.real_ip = None

    def redirect(self, link):
        # need to urlencode the bibcode only! (ie, 1973A&A....24..337S)
        link = link.replace(self.bibcode, urllib.quote(self.bibcode))
        response = redirect(link, 302)
        response.autocorrect_location_header = False
        response.headers['user_id'] = self.user_id
        return response, 302

    def process_resolver_response(self, the_json_response, log_the_click):
        """

        :param the_json_response:
        :param log_the_click: is True if we have a valid client_id and hence logging the click
        :return:
        """
        current_app.logger.info('from service got: %s'%(the_json_response))

        action = the_json_response.get('action', '')

        # when action is to redirect, there is only one link, so redirect to link
        if (action == 'redirect'):
            link = the_json_response.get('link', None)
            if link:
                link = urllib.unquote(link)
                current_app.logger.info('redirecting to %s' %(link))
                link_type = the_json_response.get('link_type', None)
                if link_type == None:
                    link_type = self.link_type
                if log_the_click:
                    log_request(self.bibcode, self.user_id, link_type, link, self.referrer, self.client_id, self.real_ip, self.user_agent)
                return self.redirect(link)

        # when action is to display, there are more than one link, so render template to display links
        if (action == 'display'):
            links = the_json_response.get('links', None)
            if links:
                records = links.get('records', None)
                if records:
                    current_app.logger.debug('rendering template with data %s' %(records))
                    if log_the_click:
                        log_request(self.bibcode, self.user_id, self.link_type, self.url, self.referrer, self.client_id, self.real_ip, self.user_agent)
                    return render_template('list.html', url="", link_type=self.link_type.title(),
                        links=records, bibcode=self.bibcode), 200

        # if we get here there is an error, so display error template
        current_app.logger.debug('The requested resource does not exist.')
        return render_template('400.html'), 400

    def get_user_info_from_adsws(self, session):
        """

        :param session:
        :return:
        """
        if session:
            try:
                current_app.logger.info('getting user info from adsws for %s' % (session))
                url = current_app.config['GATEWAY_SERVICE_ACCOUNT_INFO_URL'] + '/' + session
                headers = {'Authorization': 'Bearer ' + current_app.config['GATEWAY_TOKEN']}
                r = current_app.client.get(url=url, headers=headers)
                if r.status_code == 200:
                    current_app.logger.info('got results from adsws=%s' % (r.json()))
                    return r.json()
                current_app.logger.error('got status code from adsws=%s with message %s' % (r.status_code, r.json()))
            except HTTPError as e:
                current_app.logger.error("Http Error: %s" % (e))
            except ConnectionError as e:
                current_app.logger.error("Error Connecting: %s" % (e))
            except Exception as e:
                current_app.logger.error("Exception: %s" % (e))
        return None

    def set_user_info(self, request):
        """

        :param request:
        :return:
        """
        if request:
            self.referrer = request.referrer
            self.user_agent = request.user_agent.string
        if request.headers:
            self.real_ip = request.headers.get('x-real-ip', None)
        session = request.cookies.get('session', None)
        if session:
            try:
                account = redis_db.get(name=current_app.config['REDIS_NAME_PREFIX']+session)
            except RedisError as e:
                account = None
                current_app.logger.error('exception on getting user info from cache with session=%s: %s' % (session, str(e)))
            if account:
                current_app.logger.info('getting user info from cache with session=%s' % (session))
                # account is saved to cache as string, turned it back to dict
                account = ast.literal_eval(account)
            else:
                account = self.get_user_info_from_adsws(session)
                if account:
                    try:
                        # save it to cache
                        redis_db.set(name=current_app.config['REDIS_NAME_PREFIX']+session, value=account,
                                     ex=current_app.config['REDIS_EXPIRATION_TIME'])
                    except RedisError as e:
                        current_app.logger.error('exception on setting user info to cache with session=%s: %s' % (session, str(e)))
                else:
                    return False
            self.user_id = account['hashed_user_id']
            self.client_id = account['hashed_client_id']
            return True
        return False


    def get_request_to_service(self, params):
        """

        :param param:
        :return:
        """
        headers = {'Authorization': 'Bearer ' + current_app.config['GATEWAY_TOKEN']}
        response = current_app.client.get(url=current_app.config['GATEWAY_RESOLVER_SERVICE_URL'] % (params), headers=headers)
        return response

    def verify_link_type(self):
        """

        :return:
        """
        # while testing just return true, do not call service
        if current_app.config['TESTING']:
            return True
        # otherwise make sure link_type is valid
        response = self.get_request_to_service('check_link_type' + '/' + self.link_type)
        return response.status_code == 200

    def verify_url(self):
        """

        :return:
        """
        url = urlparse.urlparse(self.url)
        return all([url.scheme, url.netloc, url.path])

    def process_request(self):
        """

        :return:
        """
        log_the_click = False
        # log the request
        current_app.logger.info('received request with bibcode=%s and link_type=%s' %(self.bibcode, self.link_type))
        # fetch and log user info
        if self.set_user_info(request):
            # log the click only if valid user information is obtained
            log_the_click = True
            current_app.logger.info('click logging info: user_id=%s, client_id=%s, real_ip=%s'
                                    %(self.user_id, self.client_id, self.real_ip))
        if self.referrer:
            current_app.logger.info('with referrer=%s' %(self.referrer))
        if self.user_agent:
            current_app.logger.info('and user_agent=%s' %(self.user_agent))


        try:
            # if there is a url we need to log the request and redirect
            if (self.url != None):
                # make sure link_type is valid
                if self.verify_link_type():
                    # make sure we have a valid url to redirect to
                    if self.verify_url():
                        current_app.logger.debug('received to redirect to %s' %(self.url))
                        if log_the_click:
                            log_request(self.bibcode, self.user_id, self.link_type, self.url, self.referrer, self.client_id, self.real_ip, self.user_agent)
                        return self.redirect(self.url)
                    current_app.logger.error("Invalid url detected: %s" % self.url)
                    return render_template('400.html'), 400
                current_app.logger.error("Invalid link_type detected: %s" % self.link_type)
                return render_template('400.html'), 400

            # if no url then send request to resolver_service to get link(s)
            if (self.id != None):
                params = self.bibcode + '/' + self.link_type + ':' + self.id
            else:
                params = self.bibcode + '/' + self.link_type
            response = self.get_request_to_service(params)
            # need to make sure the response is json
            if (response.status_code == 200) and (response.headers.get('content-type') == 'application/json'):
                return self.process_resolver_response(response.json(), log_the_click)
            # return the error code that service has returned
            current_app.logger.error('from service got status: %d' % (response.status_code))
            return render_template('400.html'), response.status_code
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
    if url:
        url = url.lstrip(':')

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
