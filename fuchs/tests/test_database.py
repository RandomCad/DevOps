import unittest
from unittest.mock import MagicMock, patch
from psycopg import DatabaseError
from fuchs.database import DatabaseConnection


class TestDatabaseConnection(unittest.TestCase):
    @patch("fuchs.database.connect")
    def setUp(self, mock_connect):
        self.mock_conn = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.db = DatabaseConnection(
            "test_db", "test_user", "test_pass", "test_host"
        )

    def test_run_query_success(self):
        mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("title", "content", "path")

        result = self.db.run_query(lambda cur: cur.fetchone(), "Error message")
        self.assertEqual(
            result, {"status": "success", "data": ("title", "content", "path")}
        )

    def test_run_query_database_error(self):
        mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = DatabaseError("Database error")

        result = self.db.run_query(lambda cur: cur.fetchone(), "Error message")
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "server",
                "message": "Database operation failed: Database error",
            },
        )

    def test_run_query_invalid_input(self):
        mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        # Simulate a user error
        mock_cursor.fetchone.side_effect = Exception("Invalid input")
        result = self.db.run_query(lambda cur: cur.fetchone(), "Error message")
        self.assertEqual(
            result,
            {
                "status": "error",
                "type": "user",
                "message": "Invalid input: Error message",
            },
        )

    def test_run_query_error_check(self):
        mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = self.db.run_query(
            lambda cur: cur.fetchone(),
            "Error message",
            err_check=lambda ret: ret is None,
        )
        self.assertEqual(
            result, {"status": "error", "message": "Error message"}
        )


if __name__ == "__main__":
    unittest.main()
