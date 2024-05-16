# tests/test_models.py

import unittest
from tests import create_app
from app import db, models

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
       user = models.User(username='testuser')  
       user.set_password('test')  
       db.session.add(user)
       db.session.commit()
       self.assertIsNotNone(user.id)
       self.assertTrue(user.check_password('test')) 

if __name__ == '__main__':
    unittest.main()

