# -*- coding: utf-8 -*-

import sys
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(PROJECT_HOME)

import unittest
from app import app

class TestResolver(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_route(self):
        """
        Tests for the existence of a /resolver route, and that it returns
        properly formatted JSON data
        """
        r= self.app.get('/resolver/1987gady.book.....B/ABSTRACT')
        self.assertEqual(r.status_code, 302)

if __name__ == '__main__':
  unittest.main()