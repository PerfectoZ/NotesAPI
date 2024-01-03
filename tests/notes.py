import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestNotes(unittest.TestCase):
    def test_create_note(self):
        payload = {
            "title": "Test",
            "body": "Test"
        }
        response = client.post("/api/v1/notes", json=payload)
        self.assertIn("id", response.json().keys())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Test")
        self.assertEqual(response.json()["body"], "Test")

    def test_empty_title(self):
        payload = {
            "title": "",
            "body": "Test"
        }
        response = client.post("/api/v1/notes", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json().keys())

    def test_empty_body(self):
        payload = {
            "title": "Test",
            "body": ""
        }
        response = client.post("/api/v1/notes", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json().keys())


if __name__ == '__main__':
    unittest.main()
