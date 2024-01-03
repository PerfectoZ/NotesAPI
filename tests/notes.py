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

    def test_no_note(self):
        response = client.get("/api/v1/notes/100")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json().keys())

    def test_get_note(self):
        response = client.get("/api/v1/notes/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Test")
        self.assertEqual(response.json()["body"], "Test")

    def test_update_note(self):
        payload = {
            "title": "Test Update"
        }
        response = client.put("/api/v1/notes/1", json=payload)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()["title"], "Test Update")
        self.assertEqual(response.json()["body"], "Test")


if __name__ == '__main__':
    unittest.main()
