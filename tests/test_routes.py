# tests/test_routes.py

import unittest
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
