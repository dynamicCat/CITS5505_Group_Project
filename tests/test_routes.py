# tests/test_routes.py
import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from flask import url_for
from tests import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_home_route(self):
        response = self.client.get(url_for('main.home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', response.data.decode())

if __name__ == '__main__':
    unittest.main()
