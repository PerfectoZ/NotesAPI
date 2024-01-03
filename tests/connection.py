import unittest
from pymongo import MongoClient

class TestDBConnection(unittest.TestCase):
    def test_connection(self):
        client = MongoClient("mongodb://localhost:27017/")
        self.assertIsNotNone(client)
        db = client["NotesApp"]
        self.assertIsNotNone(db)
        collection = db["notes"]
        self.assertIsNotNone(collection)
        sequence = db["counters"]
        self.assertIsNotNone(sequence)

if __name__ == '__main__':
    unittest.main()
