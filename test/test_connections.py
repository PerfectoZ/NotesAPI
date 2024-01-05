import os
import unittest
from pymongo import MongoClient

class TestDBConnection(unittest.TestCase):
    def test_connection(self):
        client = MongoClient(os.getenv("DB_URL"), connectTimeoutMS=100, serverSelectionTimeoutMS=100)
        ping = client.admin.command('ping')
        self.assertIn("ok", ping)
        self.assertEqual(ping["ok"], 1)

if __name__ == '__main__':
    unittest.main()
