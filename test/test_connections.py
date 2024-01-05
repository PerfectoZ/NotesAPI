import os
import unittest
from pymongo import MongoClient
import dotenv

class TestDBConnection(unittest.TestCase):
    def test_connection(self):
        dotenv.load_dotenv(".env")
        client = MongoClient(os.getenv("DB_URL"), connectTimeoutMS=100, serverSelectionTimeoutMS=100)
        ping = client.admin.command('ping')
        self.assertIn("ok", ping)
        self.assertEqual(ping["ok"], 1)

if __name__ == '__main__':
    unittest.main()
