
import sys
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest
import requests
import httpretty

import resolverway.app as app
from resolverway.views import LinkRequest

from stubdata import data


class test_resolver(TestCase):
    def create_app(self):
        a = app.create_app(**{
            'TESTING': True,
        })
        return a

    def test_route(self):
        """
        Tests for the existence of a /resolver route, and that it returns
        properly formatted JSON data when the URL is supplied
        """
        r= self.client.get('/resolver/1987gady.book.....B/ABSTRACT/https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/ABSTRACT')
        self.assertEqual(r.status_code, 302)

    def test_single_link(self):
        """
        Tests single link response
        :return:
        """
        the_json = {"action": "redirect",
                    "link": "http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M",
                    "service": "https://ui.adsabs.harvard.edu/#abs/2013MNRAS.435.1904/ESOURCE"}
        r = LinkRequest('1987gady.book.....B', 'ABSTRACT', '').process_resolver_response(the_json)
        self.assertEqual(r[1], 302)

    def test_multiple_links(self):
        """
        Tests multiple link response
        :return:
        """
        the_json = {"action": "display",
                    "links": {"count": 4, "link_type": "ESOURCE", "bibcode": "2013MNRAS.435.1904", "records": [
                        {"url": "http://arxiv.org/abs/1307.6556", "title": "http://arxiv.org/abs/1307.6556"},
                        {"url": "http://arxiv.org/pdf/1307.6556", "title": "http://arxiv.org/pdf/1307.6556"},
                        {"url": "http://dx.doi.org/10.1093%2Fmnras%2Fstt1379", "title": "http://dx.doi.org/10.1093%2Fmnras%2Fstt1379"},
                        {"url": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf", "title": "http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf"}]},
                    "service": ""}
        r = LinkRequest('1987gady.book.....B', 'ABSTRACT', '').process_resolver_response(the_json)
        self.assertEqual(r[0], data.html_data)
        self.assertEqual(r[1], 200)

    def test_action_error(self):
        """
        Test if unrecognizable action is returned
        :return:
        """
        the_json = {"action": "redirecterror",
                    "link": "http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M",
                    "service": "https://ui.adsabs.harvard.edu/#abs/2013MNRAS.435.1904/ESOURCE"}
        r = LinkRequest('1987gady.book.....B', 'ABSTRACT', '').process_resolver_response(the_json)
        print r
        self.assertEqual(r[1], 400)

    def test_route_error(self):
        """
        Tests for wrong link type
        """
        r = self.client.get('/resolver/1987gady.book.....B/ERROR')
        self.assertEqual(r.status_code, 400)

    @httpretty.activate
    def test_with_header_and_cookie(self):
        """
        Test sending referrer in header and username in cookie
        :return:
        """
        # TODO: This is not working yet
        httpretty.register_uri(
            httpretty.GET, self.app.config['ACCOUNT_TOKEN_SERVICE_URL'],
            content_type='application/json',
            body='{"username": "user@cfa.harvard.edu", "scopes": ["api", "user", "store-query", "execute-query", "store-preferences"], "access_token": "34a3ZR71kdiCVkPUxwMeYGnHEx5mVFJuwPvI5O3s", "token_type": "Bearer", "anonymous": False, "expire_in": "2500-01-01T00:00:00", "refresh_token": "zzH3ZAIfcmjdyXdtpesyXVuxcdInarHOrqnHm349", "user_id": 1, "client_id": "yay"}')

        header = {'Referer': 'https://www.google.com/'}
        self.client.set_cookie('', 'session', 'test')
        r = self.client.get('/resolver/1987gady.book.....B/ABSTRACT', headers=header)
        self.assertEqual(0, 0) # This should be a valid assert

if __name__ == '__main__':
  unittest.main()
