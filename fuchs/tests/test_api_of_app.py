"""
This module contains unit tests for the FastAPI application defined in main.py.
It uses the FastAPI TestClient to make requests to the API endpoints and checks the responses.
"""

import unittest
from fastapi.testclient import TestClient
from fuchs.main import app


class TestApp(unittest.TestCase):
    """
    This class contains unit tests for the FastAPI application.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the TestClient for the FastAPI application.
        """
        cls.client = TestClient(app)

    def test_note_success(self):
        """
        Execute tests in the required order to simulate a successfull lifecycle
        """
        note_id = self._test_create_note()
        self._test_read_note(note_id)
        self._test_update_note(note_id)
        media_id = self._test_store_media(note_id)
        self._test_update_media(note_id, media_id)
        self._test_delete_media(note_id, media_id)
        self._test_delete_note(note_id)

    def test_note_not_found(self):
        """
        Execute tests in the required order to simulate a lifecycle with not found errors
        """
        self._test_read_note_not_found()
        self._test_update_note_not_found()
        self._test_delete_note_not_found()
        self._test_update_media_not_found()
        self._test_delete_media_not_found()

    def test_note_failure(self):
        """
        Execute tests in the required order to simulate a lifecycle with failures
        """
        self._test_create_note_failure_empty_parameter()
        self._test_create_note_failure_missing_parameter()
        note_id = self._test_create_note()
        self._test_update_note_failure_empty_parameter(note_id)
        self._test_update_note_failure_missing_parameter(note_id)
        self._test_store_media_failure_missing_parameter(note_id)
        media_id = self._test_store_media(note_id)
        self._test_update_media_failure_missing_parameter(note_id, media_id)

    def _test_create_note(self):
        """
        Test the /notes/ endpoint to ensure it creates a new note.
        """
        response = self.client.post(
            "/notes/",
            params={
                "note_title": "Test Note",
                "note_content_md": "This is a test note",
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "created")
        self.assertIn("id", response.json())
        self.assertIn("path", response.json())

        return response.json()["id"]

    def _test_create_note_failure_empty_parameter(self):
        """
        Test the /notes/ endpoint to ensure it handles failure when creating a new note.
        """
        response = self.client.post(
            "/notes/",
            params={
                "note_title": "",
                "note_content_md": "",
            },
        )
        self.assertEqual(response.status_code, 400, response.text)

    def _test_create_note_failure_missing_parameter(self):
        """
        Test the /notes/ endpoint to ensure it handles failure when creating a new note.
        """
        response = self.client.post(
            "/notes/",
            params={
                "note_title": "Test Note",
            },
        )
        self.assertEqual(response.status_code, 422, response.text)

    def _test_read_note(self, note_id: int):
        """
        Test the /notes/{note_id} endpoint to ensure it returns the content and metadata of a note.
        """
        response = self.client.get(f"/notes/{note_id}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn("id", response.json())
        self.assertIn("content", response.json())
        self.assertIn("pictures", response.json())

    def _test_read_note_not_found(self):
        """
        Test the /notes/{note_id} endpoint to ensure it handles note not found.
        """
        response = self.client.get("/notes/999")
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(
            response.json(), {"detail": "Invalid request: Note not found"}
        )

    def _test_update_note(self, note_id: int):
        """
        Test the /notes/{note_id} endpoint to ensure it updates an existing note.
        """
        url = f"/notes/{note_id}"
        response = self.client.put(
            url=url,
            params={
                "note_title": "Updated Test Note",
                "note_content_md": "This is an updated test note",
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "updated")
        self.assertEqual(response.json()["id"], note_id)

    def _test_update_note_failure_empty_parameter(self, note_id: int):
        """
        Test the /notes/{note_id} endpoint to ensure it handles failure when updating a note with empty parameters.
        """
        url = f"/notes/{note_id}"
        response = self.client.put(
            url=url,
            params={
                "note_title": "",
                "note_content_md": "",
            },
        )
        self.assertEqual(response.status_code, 400, response.text)

    def _test_update_note_failure_missing_parameter(self, note_id: int):
        """
        Test the /notes/{note_id} endpoint to ensure it handles failure when updating a note with missing parameters.
        """
        url = f"/notes/{note_id}"
        response = self.client.put(
            url=url,
            params={
                "note_title": "Updated Test Note",
            },
        )
        self.assertEqual(response.status_code, 422, response.text)

    def _test_update_note_not_found(self):
        """
        Test the /notes/{note_id} endpoint to ensure it handles note not found.
        """
        response = self.client.put(
            "/notes/999",
            params={
                "note_title": "Updated Test Note",
                "note_content_md": "This is an updated test note",
            },
        )
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(
            response.json(),
            {
                "detail": "Invalid request: Note not found",
            },
        )

    def _test_read_all_notes(self):
        """
        Test the /notes endpoint to ensure it returns a list of all notes.
        """
        response = self.client.get("/notes")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIsInstance(response.json()["notes"], list)

    def _test_store_media(self, note_id: int):
        """
        Test the /notes/{note_id}/media/ endpoint to ensure it stores a media file.
        """
        with open("tests/test_pic.png", "rb") as file:
            response = self.client.post(
                f"/notes/{note_id}/media/",
                files={"file": ("test_pic.png", file, "image/png")},
            )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "created")
        self.assertIn("id", response.json())
        self.assertIn("path", response.json())

        return response.json()["id"]

    def _test_store_media_failure_missing_parameter(self, note_id):
        """
        Test the /notes/{note_id}/media/ endpoint to ensure it handles failure when storing a media file with missing parameters.
        """
        response = self.client.post(
            f"/notes/{note_id}/media/",
            files={},
        )
        self.assertEqual(response.status_code, 422, response.text)

    def _test_update_media(self, note_id: int, media_id: int):
        """
        Test the /notes/{note_id}/media/{media_id} endpoint to ensure it updates a media file.
        """
        with open("tests/updated_test_pic.png", "rb") as file:
            response = self.client.put(
                f"/notes/{note_id}/media/{media_id}",
                files={"file": file},
            )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "updated")
        self.assertIn("path", response.json())

    def _test_update_media_failure_missing_parameter(
        self, note_id: int, media_id: int
    ):
        """
        Test the /notes/{note_id}/media/{media_id} endpoint to ensure it handles failure when updating a media file with missing parameters.
        """
        response = self.client.put(
            f"/notes/{note_id}/media/{media_id}",
            files={},
        )
        self.assertEqual(response.status_code, 422, response.text)

    def _test_update_media_not_found(self):
        """
        Test the /notes/{note_id}/media/{media_id} endpoint to ensure it handles failure when updating a media file.
        """
        with open("tests/updated_test_pic.png", "rb") as file:
            response = self.client.put(
                "/notes/999/media/999",
                files={"file": file},
            )
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(
            response.json(),
            {
                "detail": "Invalid request: Media not found",
            },
        )

    def _test_delete_media(self, note_id: int, media_id: int):
        """
        Test the /notes/{note_id}/media/{media_id} endpoint to ensure it deletes a media file.
        """
        response = self.client.delete(f"/notes/{note_id}/media/{media_id}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "deleted")

    def _test_delete_media_not_found(self):
        """
        Test the /notes/{note_id}/media/{media_id} endpoint to ensure it handles media not found.
        """
        response = self.client.delete("/notes/999/media/999")
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(
            response.json(),
            {
                "detail": "Invalid request: Media not found",
            },
        )

    def _test_delete_media_failure(self, note_id: int):
        """
        Test the /notes/{note_id}/media/{media_id} endpoint to ensure it handles failure when deleting a media file.
        """
        response = self.client.delete(f"/notes/{note_id}/media/999")
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(
            response.json(),
            {
                "status": "error",
                "message": "Invalid request: Media not found",
            },
        )

    def _test_delete_note(self, note_id: int):
        """
        Test the /notes/{note_id} endpoint to ensure it deletes an existing note.
        """
        response = self.client.delete(f"/notes/{note_id}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "deleted")

    def _test_delete_note_not_found(self):
        """
        Test the /notes/{note_id} endpoint to ensure it handles note not found.
        """
        response = self.client.delete("/notes/999")
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(
            response.json(), {"detail": "Invalid request: Note not found"}
        )


if __name__ == "__main__":
    unittest.main()
