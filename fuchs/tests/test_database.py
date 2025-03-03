import unittest
from unittest.mock import patch, MagicMock
from fuchs.database import DatabaseConnection

class TestDatabaseConnection(unittest.TestCase):

    @patch('fuchs.database.psycopg2.connect')
    def setUp(self, mock_connect):
        self.mock_conn = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.db = DatabaseConnection('dbname', 'user', 'password', 'host')

    def test_read_note_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = ('Test Title', 'Test Content', 'Test Path')
        
        result = self.db.read_note(1)
        
        self.assertEqual(result, ('Test Title', 'Test Content', 'Test Path'))
        mock_cursor.execute.assert_called_once_with(
            "SELECT note_title, note_content, note_path FROM notes WHERE note_id = %s", (1,)
        )

    def test_read_all_notes_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [(1, 'Test Title')]
        
        result = self.db.read_all_notes()
        
        self.assertEqual(result, [(1, 'Test Title')])
        mock_cursor.execute.assert_called_once_with("SELECT note_id, note_title FROM notes")

    def test_write_note_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = [1]
        
        result = self.db.write_note('Test Title', 'Test Content', 'Test Path')
        
        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO notes (note_title, note_content, note_path) VALUES (%s, %s, %s) RETURNING note_id",
            ('Test Title', 'Test Content', 'Test Path')
        )

    def test_update_note_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1
        
        result = self.db.update_note(1, 'Updated Title', 'Updated Content', 'Updated Path')
        
        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once_with(
            "UPDATE notes SET note_title = %s, note_content = %s, note_path = %s WHERE note_id = %s",
            ('Updated Title', 'Updated Content', 'Updated Path', 1)
        )

    def test_remove_note_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1
        
        result = self.db.remove_note(1)
        
        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once_with("DELETE FROM notes WHERE note_id = %s", (1,))

    def test_store_meta_of_picture_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = [1]
        
        result = self.db.store_meta_of_picture(1, 'Pic Name', 'Pic Alt Text', 'Pic Path')
        
        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO pictures (note_id, picture_name, picture_alt_text, picture_path) VALUES (%s, %s, %s, %s) RETURNING picture_id",
            (1, 'Pic Name', 'Pic Alt Text', 'Pic Path')
        )

    def test_read_meta_of_picture_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (1, 'Pic Name', 'Pic Alt Text', 'Pic Path')
        
        result = self.db.read_meta_of_picture(1)
        
        self.assertEqual(result, (1, 'Pic Name', 'Pic Alt Text', 'Pic Path'))
        mock_cursor.execute.assert_called_once_with(
            "SELECT note_id, picture_name, picture_alt_text, picture_path FROM pictures WHERE picture_id = %s",
            (1,)
        )

    def test_remove_meta_of_picture_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1
        
        result = self.db.remove_meta_of_picture(1)
        
        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once_with("DELETE FROM pictures WHERE picture_id = %s", (1,))

    def test_read_all_meta_of_pictures_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [(1, 'Pic Name', 'Pic Alt Text', 'Pic Path')]
        
        result = self.db.read_all_meta_of_pictures(1)
        
        self.assertEqual(result, [(1, 'Pic Name', 'Pic Alt Text', 'Pic Path')])
        mock_cursor.execute.assert_called_once_with(
            "SELECT picture_id, picture_name, picture_alt_text, picture_path FROM pictures WHERE note_id = %s",
            (1,)
        )

    def test_update_meta_of_picture_success(self):
        mock_cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1
        
        result = self.db.update_meta_of_picture(1, 'Updated Pic Name', 'Updated Pic Alt Text', 'Updated Pic Path')
        
        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once_with(
            "UPDATE pictures SET (picture_name = %s, picture_alt_text = %s, picture_path = %s) WHERE picture_id = %s",
            ('Updated Pic Name', 'Updated Pic Alt Text', 'Updated Pic Path', 1)
        )

if __name__ == '__main__':
    unittest.main()
