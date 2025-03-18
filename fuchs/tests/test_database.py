import unittest
from unittest.mock import patch, MagicMock
from fuchs import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from fuchs.database import DatabaseConnection, get_db


class TestDatabaseConnection(unittest.TestCase):
    @patch("fuchs.database.psycopg2.connect")
    def setUp(self, mock_connect):
        self.mock_conn = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.db = next(get_db())

    def test_read_note_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (
            "Test Title",
            "Test Content",
            "Test Path",
        )

        result = self.db.read_note(1)

        self.assertEqual(
            result,
            {
                "status": "success",
                "data": ("Test Title", "Test Content", "Test Path"),
            },
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT note_title, note_content, note_path FROM notes WHERE note_id = %s",
            (1,),
        )

    def test_read_note_not_found(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None

        result = self.db.read_note(999)

        self.assertEqual(
            result, {"status": "error", "message": "Note not found"}
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT note_title, note_content, note_path FROM notes WHERE note_id = %s",
            (999,),
        )

    def test_read_note_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.read_note(1)
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_read_all_notes_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [(1, "Test Title")]

        result = self.db.read_all_notes()

        self.assertEqual(
            result, {"status": "success", "data": [(1, "Test Title")]}
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT note_id, note_title FROM notes"
        )

    def test_read_all_notes_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.read_all_notes()
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_write_note_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = [1]

        result = self.db.write_note("Test Title", "Test Content", "Test Path")

        self.assertEqual(result, {"status": "success", "data": 1})
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO notes (note_title, note_content, note_path) VALUES (%s, %s, %s) RETURNING note_id",
            ("Test Title", "Test Content", "Test Path"),
        )

    def test_write_note_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.write_note("Test Title", "Test Content", "Test Path")
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_update_note_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1

        result = self.db.update_note(
            1, "Updated Title", "Updated Content", "Updated Path"
        )

        self.assertEqual(result, {"status": "success", "data": 1})
        mock_cursor.execute.assert_called_once_with(
            "UPDATE notes SET note_title = %s, note_content = %s, note_path = %s WHERE note_id = %s",
            ("Updated Title", "Updated Content", "Updated Path", 1),
        )

    def test_update_note_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.update_note(
            1, "Updated Title", "Updated Content", "Updated Path"
        )
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_remove_note_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1

        result = self.db.remove_note(1)

        self.assertEqual(result, {"status": "success", "data": 1})
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM notes WHERE note_id = %s", (1,)
        )

    def test_remove_note_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.remove_note(1)
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_store_meta_of_media_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = [1]

        result = self.db.store_meta_of_media(1, "Media Name")

        self.assertEqual(result, {"status": "success", "data": 1})
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO media (note_id, media_name, media_path) VALUES (%s, %s, %s) RETURNING media_id",
            (1, "Media Name", ""),
        )

    def test_store_meta_of_media_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.store_meta_of_media(1, "Media Name")
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_read_meta_of_media_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (1, "Media Name", "Media Path")

        result = self.db.read_meta_of_media(1)

        self.assertEqual(
            result,
            {"status": "success", "data": (1, "Media Name", "Media Path")},
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT note_id, media_name, media_path FROM media WHERE media_id = %s",
            (1,),
        )

    def test_read_meta_of_media_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.read_meta_of_media(1)
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_read_meta_of_media_not_found(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None

        result = self.db.read_meta_of_media(999)

        self.assertEqual(
            result, {"status": "error", "message": "Media not found"}
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT note_id, media_name, media_path FROM media WHERE media_id = %s",
            (999,),
        )

    def test_remove_meta_of_media_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1

        result = self.db.remove_meta_of_media(1)

        self.assertEqual(result, {"status": "success", "data": 1})
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM media WHERE media_id = %s", (1,)
        )

    def test_remove_meta_of_media_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.remove_meta_of_media(1)
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_read_all_meta_of_media_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [(1, "Media Name", "Media Path")]

        result = self.db.read_all_meta_of_media(1)

        self.assertEqual(
            result,
            {"status": "success", "data": [(1, "Media Name", "Media Path")]},
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT media_id, media_name, media_path FROM media WHERE note_id = %s",
            (1,),
        )

    def test_read_all_meta_of_media_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.read_all_meta_of_media(1)
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    def test_update_meta_of_media_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1

        result = self.db.update_meta_of_media(
            1, "Updated Media Name", "Updated Media Path"
        )

        self.assertEqual(result, {"status": "success", "data": 1})
        mock_cursor.execute.assert_called_once_with(
            "UPDATE media SET media_name = %s, media_path = %s WHERE media_id = %s",
            ("Updated Media Name", "Updated Media Path", 1),
        )

    def test_update_meta_of_media_exception(self):
        self.mock_conn.cursor.side_effect = Exception("Invalid input")
        result = self.db.update_meta_of_media(
            1, "Updated Media Name", "Updated Media Path"
        )
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Invalid input",
            },
        )

    @patch("fuchs.database.psycopg2.connect")
    def test_get_db(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        db_gen = get_db()
        db = next(db_gen)

        self.assertIsInstance(db, DatabaseConnection)
        mock_connect.assert_called_once_with(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
        )

        db_gen.close()
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
