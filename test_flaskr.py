import unittest
import json

from flaskr import create_app
from models import setup_db

#Create Test Case
class CastingAppTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capdb_test"
        self.database_path = "postgresql://postgres:pgpw@localhost:5432/{}".format(self.database_name)
        setup_db(self.app, self.database_path)
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()