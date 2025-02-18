"""This module provides a class to connect to a PostgreSQL database and
provides methods to write, read and update notes"""
import psycopg2


class DatabaseConnection:
    """connects to a PostgreSQL database and provides methods to write, read
    and update notes"""

    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )

    def __del__(self):
        self.conn.close()

    def write_note(self, content: str):
        """writes a new note to the database,
        returns the id of the new note"""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notes (content) VALUES (%s) RETURNING id",
                (content)
            )
            return cur.fetchone()[0]

    def read_note(self, note_id: int):
        """reads a note from the database by id,
        returns a tuple with the title and content of the note"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT title, content FROM notes WHERE id = %s",
                (note_id)
            )
            return cur.fetchone()

    def update_note(self, note_id: int, content: str):
        """updates a note in the database by id,
        returns the number of rows affected"""
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE notes SET content = %s WHERE id = %s",
                (content, note_id)
            )
            return cur.rowcount

    def remove_note(self, note_id: int):
        """removes a note from the database by id,
        returns the number of rows affected"""
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM notes WHERE id = %s",
                (note_id)
            )
            return cur.rowcount
