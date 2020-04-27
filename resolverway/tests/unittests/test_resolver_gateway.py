
import sys
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest
import Cookie


import resolverway.app as app
from resolverway.views import LinkRequest, redis_db

from stubdata import data


class test_resolver(TestCase):
    def create_app(self):
        self.current_app = app.create_app(**{'TESTING': True})
        return self.current_app

    def test_route(self):
        """
        Tests for the existence of a /link_gateway route, and that it returns
        properly formatted JSON data when the URL is supplied
        """
        r= self.client.get('/link_gateway/1987gady.book.....B/ABSTRACT/https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/ABSTRACT')
        self.assertEqual(r.status_code, 302)

    def test_route_error_invalid_url(self):
        """
        test that if given invalid url returns error
        :return:
        """

        r = self.client.get('/link_gateway/1987gady.book.....B/ABSTRACT/invalid_url')
        self.assertEqual(r.status_code, 400)

    def test_single_link(self):
        """
        Tests single link response
        :return:
        """
        the_json = {"action": "redirect",
                    "link": "http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M",
                    "service": "https://ui.adsabs.harvard.edu/#abs/2013MNRAS.435.1904/ESOURCE"}
        r = LinkRequest('1987gady.book.....B', 'ABSTRACT', '').process_resolver_response(the_json, True)
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
        r = LinkRequest('1987gady.book.....B', 'ABSTRACT', '').process_resolver_response(the_json, False)
        self.assertEqual(r[0], data.html_data)
        self.assertEqual(r[1], 200)

    def test_identification_link(self):
        """
        Tests single link response for identification link types
        :return:
        """
        the_json = {"action": "redirect",
                    "link": "http://dx.doi.org/10.1088/2041-8205/713/2/L10",
                    "service": "https://ui.adsabs.harvard.edu/#abs/2010ApJ...713L.103B/DOI:10.1088/2041-8205/713/2/L103"}
        r = LinkRequest('2010ApJ...713L.103B', 'DOI', '10.1088,2041-8205,713,2,L10').process_resolver_response(the_json, True)
        self.assertEqual(r[1], 302)

        the_json = {"action": "redirect",
                    "link": "http://arxiv.org/abs/1803.03598",
                    "service": "https://ui.adsabs.harvard.edu/#abs/2018arXiv180303598K/ARXIV:1803.03598"}
        r = LinkRequest('2018arXiv180303598K', 'ARXIV', '1803.03598').process_resolver_response(the_json, False)
        self.assertEqual(r[1], 302)

    def test_action_error(self):
        """
        Test if unrecognizable action is returned
        :return:
        """
        the_json = {"action": "redirecterror",
                    "link": "http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M",
                    "service": "https://ui.adsabs.harvard.edu/#abs/2013MNRAS.435.1904/ESOURCE"}
        r = LinkRequest('1987gady.book.....B', 'ABSTRACT', '').process_resolver_response(the_json, True)
        self.assertEqual(r[1], 400)

    def test_route_error_invalid_link_type(self):
        """
        Tests for wrong link type
        """
        r = self.client.get('/link_gateway/1987gady.book.....B/ERROR')
        self.assertNotEquals(r.status_code, 200)

    def test_with_header_info(self):
        """
        Test sending referrer in header and getting user info
        :return:
        """
        header = {'Referer': 'https://www.google.com/'}
        r = self.client.get('/link_gateway/1987gady.book.....B/ABSTRACT/https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/ABSTRACT', headers=header)
        self.assertEqual(r.status_code, 302)

    def test_redis_available(self):
        """
        Test that redis available
        :return:
        """
        # Test that redis is available
        self.assertNotEqual(self.current_app.extensions['redis'], None)

    def test_redis_put_get(self):
        """
        add an entry to redis, pass the same session id and verify that it was fetched
        next do not pass session id and verifty that it was not fetched
        :return:
        """
        # add an entry
        account1 = {"source": "session:client_id", "hashed_client_id": "013c1b1280353b3319133b9c528fb29ba998ae3b7af9b669166a786bc6796c9d", "anonymous": True, "hashed_user_id": "ec43c30b9a81ed89765a2b8a04cac38925058eeacd5b5264389b1d4a7df2b28c"}
        self.current_app.extensions['redis'].set(self.current_app.config['REDIS_NAME_PREFIX']+'key1', account1)

        # verify that when the same session id is passed as cookie, the entry was fetched from redis
        header = {'cookie': 'session=key1', 'x-real-ip': '0.0.0.0'}
        r = self.client.get('/link_gateway/2018AAS...23130709A/ABSTRACT/https://ui.adsabs.harvard.edu/#abs/2018AAS...23130709A/ABSTRACT', headers=header)
        self.assertEqual(r.headers['user_id'], 'ec43c30b9a81ed89765a2b8a04cac38925058eeacd5b5264389b1d4a7df2b28c')

        # verify that when no cookie is send, session_id is None
        r = self.client.get('/link_gateway/2018AAS...23130709A/ABSTRACT/https://ui.adsabs.harvard.edu/#abs/2018AAS...23130709A/ABSTRACT')
        self.assertEqual(r.headers['user_id'], 'None')

    def test_redis_exception(self):
        """
        set max_connections to 1 and close it, now try to fetch the key to get exception
        :return:
        """
        self.current_app.extensions['redis']._redis_client.connection_pool.max_connections = 0
        self.current_app.extensions['redis']._redis_client.connection_pool.disconnect()
        header = {'cookie': 'session=key1', 'x-real-ip': '0.0.0.0'}
        r = self.client.get('/link_gateway/2018AAS...23130709A/ABSTRACT/https://ui.adsabs.harvard.edu/#abs/2018AAS...23130709A/ABSTRACT', headers=header)
        self.assertEqual(r.headers['user_id'], 'None')

    def test_adsws_call(self):
        """

        :return:
        """
        account = LinkRequest('2018AAS...23130709A', 'ABSTRACT', 'https://ui.adsabs.harvard.edu/#abs/2018AAS...23130709A/ABSTRACT').get_user_info_from_adsws(None)
        self.assertEqual(account, None)


if __name__ == '__main__':
  unittest.main()
