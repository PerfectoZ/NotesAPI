import os
import unittest
import dotenv

class MyTestCase(unittest.TestCase):
    def test_something(self):
        dotenv.load_dotenv()
        self.assertIsInstance(os.environ['DB_URL'], str)
        self.assertIsNotNone(os.environ['DB_URL'])
        self.assertIsNotNone(os.environ['DB_NAME'])
        self.assertIsNotNone(os.environ['DB_COLLECTION'])
        self.assertIsNotNone(os.environ['DB_SEQUENCE'])
        self.assertIsNotNone(os.environ['DB_SHARING'])
        self.assertIsNotNone(os.environ['TOKEN_GEN_ALGORITHM'])
        self.assertIsNotNone(os.environ['TOKEN_EXPIRY_DURATION_MINUTES'])
        self.assertIsNotNone(os.environ['TOKEN_SECRET_KEY'])

if __name__ == '__main__':
    unittest.main()
