
from flask import current_app, request, Blueprint, Response, redirect, render_template
from flask_discoverer import advertise
from flask import Response
import requests

from resolverway.log import log_request

bp = Blueprint('resolver_gateway', __name__)

class LinkRequest():

    bibcode = ''
    link_type = ''
    link_sub_type = ''
    url = ''
    username = ''

    def __init__(self, bibcode, link_type, url):
        self.bibcode = bibcode
        self.link_type = link_type
        self.url = url


    def __return_response_error(self, response, status):
        current_app.logger.info('sending response status=%s' %(status))
        current_app.logger.info('sending response text=%s' %(response))

        r = Response(response=response, status=status)
        r.headers['content-type'] = 'text/plain; charset=UTF-8'
        return r


    def __log_request_info(self):
        current_app.logger.info('received request with bibcode=%s and link_type=%s' %(self.bibcode, self.link_type))
        if self.username:
            current_app.logger.info('and username=%s' %(self.username))
        if self.referrer:
            current_app.logger.info('also referrer=%s' %(self.referrer))


    def process_request(self):
        """

        :return:
        """
        self.username = request.cookies.get('username', '')
        self.referrer = request.referrer

        self.__log_request_info()

        # if there is a url we need to log the request and redirect
        if (self.url != None):
            current_app.logger.debug('received to redirect to %s' %(self.url))
            return redirect(self.url, 302)

        params = self.bibcode + '/' + self.link_type
        response = requests.get(url=current_app.config['RESOLVER_SERVICE_URL'].format(params), headers=request.headers)

        contentType = response.headers.get('content-type')

        # need to make sure the response is json
        if (contentType == 'application/json'):
            the_json_response = response.json()
            print 'the_json_response=', the_json_response
            action = the_json_response.get('action', '')
            # when action is to redirect, there is only one link
            if (action == 'redirect'):
                link = the_json_response['link']                
                current_app.logger.info('redirecting to %s' %(link))
                return redirect(link, 302)
            # when action is to display, there is more than one link
            elif (action == 'display'):
                links = the_json_response['links']
                log_request(self.bibcode, self.username, self.link_type, self.url, self.referrer)
                current_app.logger.debug('rendering template with data %s' %(links))
                return render_template('list.html', link_type=self.link_type.title(),
                    links=links, bibcode=self.bibcode)

        return self.__return_response_error(response='', status=404)


@advertise(scopes=[], rate_limit=[1000, 3600 * 24])
@bp.route('/<bibcode>/<link_type>', defaults={'url': None}, methods=['GET'])
@bp.route('/<bibcode>/<link_type>/<path:url>', methods=['GET'])
def resolver(bibcode, link_type, url):
    return LinkRequest(bibcode, link_type.upper(), url).process_request()



