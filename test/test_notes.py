import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from fastapi import HTTPException
from models.Note import NoteCreate, NoteDB, NoteUpdate

class TestNoteController(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("controllers.NoteController.noteService.create_note_service")
    def test_create_note(self, create_note_service_mock):
        create_note_service_mock.return_value = NoteDB(id=1, title="Test", body="Test")
        response = self.client.post("/api/v1/notes", json={"title": "Test", "body": "Test"})
        assert response.status_code == 201
        assert response.json() == {"id": 1, "title": "Test", "body": "Test"}
        create_note_service_mock.assert_called_once_with(NoteCreate(title="Test", body="Test"))

    @patch("controllers.NoteController.noteService.create_note_service")
    def test_empty_title(self, create_note_service_mock):
        create_note_service_mock.side_effect = ValueError("Title cannot be empty")
        payload = {"title": "", "body": "Test"}
        response = self.client.post("/api/v1/notes", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json().keys())
        create_note_service_mock.assert_not_called()

    @patch("controllers.NoteController.noteService.create_note_service")
    def test_empty_body(self, create_note_service_mock):
        create_note_service_mock.side_effect = ValueError("Body cannot be empty")
        payload = {"title": "Test", "body": ""}
        response = self.client.post("/api/v1/notes", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json().keys())
        create_note_service_mock.assert_not_called()

    @patch("controllers.NoteController.noteService.get_note_service")
    def test_no_note(self, get_note_service_mock):
        get_note_service_mock.side_effect = HTTPException(detail="Note not found", status_code=404)
        response = self.client.get("/api/v1/notes/1")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json().keys())
        get_note_service_mock.assert_called_once_with(1)

    @patch("controllers.NoteController.noteService.create_note_service")
    @patch("controllers.NoteController.noteService.get_note_service")
    def test_get_note(self, get_note_service_mock, create_note_service_mock):
        created_note = NoteDB(id=1, title="Test", body="Test")
        create_note_service_mock.return_value = created_note

        create_response = self.client.post("/api/v1/notes", json={"title": "Test", "body": "Test"})
        create_note_service_mock.assert_called_once()

        get_note_service_mock.reset_mock()
        get_note_service_mock.return_value = created_note

        get_response = self.client.get(f'/api/v1/notes/{create_response.json()["id"]}')
        get_note_service_mock.assert_called_once_with(created_note.id)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["title"], "Test")
        self.assertEqual(get_response.json()["body"], "Test")

    @patch("controllers.NoteController.noteService.create_note_service")
    @patch("controllers.NoteController.noteService.update_note_service")
    def test_update_note(self, update_note_service_mock, create_note_service_mock):
        created_note = NoteDB(id=1, title="Test", body="Test")
        create_note_service_mock.return_value = created_note
        create_response = self.client.post("/api/v1/notes", json={"title": "Test", "body": "Test"})
        create_note_service_mock.assert_called_once()

        update_note_service_mock.reset_mock()

        updated_note = NoteDB(id=1, title="Test Update", body="Test")
        update_note_service_mock.return_value = updated_note

        update_payload = {"title": "Test Update"}
        update_response = self.client.put(f'/api/v1/notes/{create_response.json()["id"]}', json=update_payload)
        update_note_service_mock.assert_called_once_with(1, NoteUpdate(title="Test Update"))

        self.assertEqual(update_response.status_code, 202)
        self.assertEqual(update_response.json()["title"], "Test Update")
        self.assertEqual(update_response.json()["body"], "Test")

    @patch("controllers.NoteController.noteService.create_note_service")
    @patch("controllers.NoteController.noteService.delete_note_service")
    def test_delete_note(self, delete_note_service_mock, create_note_service_mock):
        created_note = NoteDB(id=1, title="Test", body="Test")
        create_note_service_mock.return_value = created_note

        create_response = self.client.post("/api/v1/notes", json={"title": "Test", "body": "Test"})
        create_note_service_mock.assert_called_once()

        delete_note_service_mock.reset_mock()

        delete_note_service_mock.return_value = {"message": "Deleted Successfully"}

        delete_response = self.client.delete(f'/api/v1/notes/{create_response.json()["id"]}')
        delete_note_service_mock.assert_called_once_with(1)

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.json()["message"], "Deleted Successfully")

if __name__ == "__main__":
    unittest.main()
