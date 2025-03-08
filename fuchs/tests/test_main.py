import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fuchs.main import app
from fuchs.database import get_db, DatabaseConnection

class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Override the get_db dependency
        app.dependency_overrides[get_db] = lambda: cls.mock_db

        cls.client = TestClient(app)
        cls.mock_db = MagicMock(spec=DatabaseConnection)
        cls.mock_db_context = patch('fuchs.main.get_db', return_value=cls.mock_db)
        cls.mock_db_context.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_db_context.stop()
        # Remove the dependency override
        app.dependency_overrides = {}

    def test_read_all_notes(self):
        self.mock_db.read_all_notes.return_value = [(1, "Test Note")]
        response = self.client.get("/notes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"notes": [{"id": 1, "title": "Test Note"}]})

    def test_read_note_success(self):
        self.mock_db.read_note.return_value = ("Test Note", "Test Content", "Test Path")
        self.mock_db.read_all_meta_of_media.return_value = [(1, "media_path")]
        response = self.client.get("/notes/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "title": "Test Note",
            "content": "Test Content",
            "path": "Test Path",
            "pictures": [{"id": 1, "path": "media_path"}]
        })

    def test_read_note_not_found(self):
        self.mock_db.read_note.return_value = None
        response = self.client.get("/notes/999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "error", "message": "Note with id 999 not found"})

    def test_create_note_success(self):
        self.mock_db.write_note.return_value = 1
        self.mock_db.update_note.return_value = 1
        with patch('fuchs.main.convert_md_to_html', return_value="HTML Content"):
            with patch('fuchs.main.put_file_on_hamster') as mock_put_file:
                response = self.client.post("/notes/", params={"note_title": "Test Note", "note_content_md": "Test Content"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"status": "created", "id": 1, "path": "note_1/web.html"})
                mock_put_file.assert_called_once_with("note_1/web.html", "HTML Content")

    def test_create_note_failure(self):
        self.mock_db.write_note.return_value = None
        response = self.client.post("/notes/", params={"note_title": "Test Note", "note_content_md": "Test Content"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "error", "message": "Failed to create note"})

    def test_update_note_success(self):
        self.mock_db.read_note.return_value = ("Test Note", "Test Content", "note_1/web.html")
        self.mock_db.update_note.return_value = 1
        with patch('fuchs.main.convert_md_to_html', return_value="Updated HTML Content"):
            with patch('fuchs.main.put_file_on_hamster') as mock_put_file:
                response = self.client.put("/notes/1", params={"note_title": "Updated Note", "note_content_md": "Updated Content"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"status": "updated", "id": 1})
                mock_put_file.assert_called_once_with("note_1/web.html", "Updated HTML Content")

    def test_update_note_not_found(self):
        self.mock_db.read_note.return_value = None
        response = self.client.put("/notes/999", params={"note_title": "Updated Note", "note_content_md": "Updated Content"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "error", "message": "Note with id 999 not found"})

    def test_delete_note_success(self):
        self.mock_db.read_note.return_value = ("Test Note", "Test Content", "note_1/web.html")
        self.mock_db.remove_note.return_value = 1
        with patch('fuchs.main.delete_file_on_hamster') as mock_delete_file:
            response = self.client.delete("/notes/1")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "deleted"})
            mock_delete_file.assert_called_once_with("note_1/web.html")

    def test_delete_note_not_found(self):
        self.mock_db.read_note.return_value = None
        response = self.client.delete("/notes/999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "error", "message": "Note with id 999 not found"})

    def test_store_media_success(self):
        self.mock_db.store_meta_of_media.return_value = 1
        self.mock_db.update_meta_of_media.return_value = 1
        with patch('fuchs.main.put_file_on_hamster') as mock_put_file:
            with open("tests/test_pic.png", "rb") as file:
                response = self.client.post("/notes/1/media/", files={"file": ("test_pic.png", file, "image/png")})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"status": "created", "id": 1, "path": "note_1/media/1"})
                mock_put_file.assert_called_once()

    def test_store_media_failure(self):
        self.mock_db.store_meta_of_media.return_value = None
        with open("tests/test_pic.png", "rb") as file:
            response = self.client.post("/notes/1/media/", files={"file": ("test_pic.png", file, "image/png")})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "error", "message": "Failed to store media"})

    def test_update_media_success(self):
        self.mock_db.read_meta_of_media.return_value = (1, "media_name", "note_1/media/1")
        self.mock_db.update_meta_of_media.return_value = 1
        with patch('fuchs.main.put_file_on_hamster') as mock_put_file:
            with open("tests/updated_test_pic.png", "rb") as file:
                response = self.client.put("/notes/1/media/1", files={"file": file})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"status": "updated", "path": "note_1/media/1"})
                mock_put_file.assert_called_once()

    def test_update_media_not_found(self):
        self.mock_db.read_meta_of_media.return_value = None
        with open("tests/updated_test_pic.png", "rb") as file:
            response = self.client.put("/notes/1/media/999", files={"file": file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "error", "message": "Media with id 999 and note 1 not found"})

    def test_delete_media_success(self):
        self.mock_db.read_meta_of_media.return_value = (1, "media_name", "note_1/media/1")
        self.mock_db.remove_meta_of_media.return_value = 1
        with patch('fuchs.main.delete_file_on_hamster') as mock_delete_file:
            response = self.client.delete("/notes/1/media/1")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "deleted"})
            mock_delete_file.assert_called_once_with("note_1/media/1")

    def test_delete_media_not_found(self):
        self.mock_db.read_meta_of_media.return_value = None
        response = self.client.delete("/notes/1/media/999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "error", "message": "Media with id 999 and note 1 not found"})

if __name__ == "__main__":
    unittest.main()
