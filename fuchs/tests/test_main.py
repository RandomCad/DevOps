"""
This module contains unit tests for the FastAPI application defined in main.py.
It uses the FastAPI TestClient to make requests to the API endpoints and checks the responses.
"""

import unittest

from fastapi.testclient import TestClient

from fuchs.main import app


class TestMain(unittest.TestCase):
    """
    This class contains unit tests for the FastAPI application.
    """

    test_note_id = None
    test_note_pic_id = None

    @classmethod
    def setUpClass(cls):
        """
        Set up the TestClient for the FastAPI application.
        """
        cls.client = TestClient(app)

    def test_create_note_and_related_operations(self):
        """
        Execute tests in the required order.
        """
        self._test_create_note()
        self._test_read_note()
        self._test_update_note()
        # self._test_store_picture()
        # self._test_update_picture()
        # self._test_delete_picture()
        self._test_delete_note()

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

        self.test_note_id = response.json()["id"]

    def _test_read_note(self):
        """
        Test the /notes/{note_id} endpoint to ensure it returns the content and metadata of a note.
        """
        response = self.client.get(f"/notes/{self.test_note_id}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn("id", response.json())
        self.assertIn("content", response.json())
        self.assertIn("pictures", response.json())

    def _test_update_note(self):
        """
        Test the /notes/{note_id} endpoint to ensure it updates an existing note.
        """
        url = f"/notes/{self.test_note_id}"
        response = self.client.put(
            url=url,
            params={
                "note_title": "Updated Test Note",
                "note_content_md": "This is a updated test note",
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "updated")
        self.assertEqual(response.json()["id"], self.test_note_id)

    def _test_read_all_notes(self):
        """
        Test the /notes endpoint to ensure it returns a list of all notes.
        """
        response = self.client.get("/notes")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIsInstance(response.json()["notes"], list)

    def _test_store_picture(self):
        """
        Test the /notes/{note_id}/pics/ endpoint to ensure it stores a picture.
        """
        response = self.client.post(
            f"/notes/{self.test_note_id}/pics/",
            params={
                "pic_content": "Test Picture Content",
                "pic_name": "test_pic.jpg",
                "pic_alt_text": "Test Picture",
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "created")
        self.assertIn("id", response.json())
        self.assertIn("path", response.json())

        self.test_note_pic_id = response.json()["id"]

    def _test_update_picture(self):
        """
        Test the /notes/{note_id}/pics/{pic_id} endpoint to ensure it updates a picture.
        """
        response = self.client.put(
            f"/notes/{self.test_note_id}/pics/{self.test_note_pic_id}",
            params={
                "pic_id": 1,
                "pic_content": "Updated Test Picture Content",
                "pic_name": "updated_test_pic.jpg",
                "pic_alt_text": "Updated Test Picture",
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "updated")
        self.assertIn("path", response.json())

    def _test_delete_picture(self):
        """
        Test the /notes/{note_id}/pics/{pic_id} endpoint to ensure it deletes a picture.
        """
        response = self.client.delete(
            f"/notes/{self.test_note_id}/pics/{self.test_note_pic_id}"
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "deleted")

    def _test_delete_note(self):
        """
        Test the /notes/{note_id} endpoint to ensure it deletes an existing note.
        """
        response = self.client.delete(f"/notes/{self.test_note_id}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "deleted")


if __name__ == "__main__":
    unittest.main()
