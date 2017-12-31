
import sys
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest

import resolverway.app as app

class test_resolver(TestCase):
    def create_app(self):
        self.current_app = app.create_app()
        return self.current_app

    def test_route(self):
        """
        Tests for the existence of a /resolver route, and that it returns
        properly formatted JSON data when the URL is supplied
        """
        r= self.client.get('/1987gady.book.....B/ABSTRACT/https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/ABSTRACT')
        self.assertEqual(r.status_code, 302)

    def test_route_error(self):
        """
        Tests for wrong link type
        """
        r = self.client.get('/1987gady.book.....B/ERROR')
        self.assertEqual(r.status_code, 400)


if __name__ == '__main__':
  unittest.main()