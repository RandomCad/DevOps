"""This module provides a class to connect to a PostgreSQL database and
provides methods to write, read and update notes"""

import psycopg2


class DatabaseConnection:
    """connects to a PostgreSQL database and provides methods to write, read
    and update notes"""

    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host
        )

    def read_note(self, note_id: int):
        """reads a note from the database by id,
        returns a tuple with the title and content of the note"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT note_title, note_content, note_path FROM notes WHERE note_id = %s",
                    (note_id,),
                )
                ret = cur.fetchone()
        return ret

    def read_all_notes(self):
        """reads all notes from the database,
        returns a list of tuples with the title and id of the notes"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT note_id, note_title FROM notes")
                ret = cur.fetchall()
        return ret

    def write_note(self, title: str, content: str, path: str = ""):
        """writes a new note to the database,
        returns the id of the new note"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO notes (note_title, note_content, note_path) VALUES (%s, %s, %s) RETURNING note_id",
                    (title, content, path),
                )
                ret = cur.fetchone()[0]
        return ret

    def update_note(self, note_id: int, title: str, content: str, path: str):
        """updates a note in the database by id,
        returns the number of rows affected"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "UPDATE notes SET note_title = %s, note_content = %s, note_path = %s WHERE note_id = %s",
                    (title, content, path, note_id),
                )
                ret = cur.rowcount
        return ret

    def remove_note(self, note_id: int):
        """removes a note from the database by id,
        returns the number of rows affected"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM notes WHERE note_id = %s", (note_id,))
                ret = cur.rowcount
        return ret

    def store_meta_of_picture(
        self, note_id: int, pic_name: str, pic_alt_text: str, pic_path: str
    ):
        """stores the reference between a piv and a note,
        returns the id of the picture"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO pictures (note_id, picture_name, picture_alt_text, picture_path) VALUES (%s, %s, %s, %s) RETURNING picture_id",
                    (note_id, pic_name, pic_alt_text, pic_path),
                )
                ret = cur.fetchone()[0]
        return ret

    def read_meta_of_picture(self, pic_id: int):
        """reads the meta information of a picture by id,
        returns a tuple with the note_id, name and alt_text of the picture"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT note_id, picture_name, picture_alt_text, picture_path FROM pictures WHERE picture_id = %s",
                    (pic_id,),
                )
                ret = cur.fetchone()
        return ret

    def remove_meta_of_picture(self, pic_id: int):
        """removes a picture from the database by id,
        returns the number of rows affected"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM pictures WHERE picture_id = %s", (pic_id,))
                ret = cur.rowcount
        return ret

    def read_all_meta_of_pictures(self, note_id: int):
        """reads all pictures of a note by id,\n
        returns a list of tuples with the id, name, alt_text and path of the
        pictures"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT picture_id, picture_name, picture_alt_text, picture_path FROM pictures WHERE note_id = %s",
                    (note_id,),
                )
                ret = cur.fetchall()
        return ret

    def update_meta_of_picture(
        self, pic_id: int, pic_name: str, pic_alt_text: str, pic_path: str
    ):
        """updates the meta information of a picture by id,
        returns the number of rows affected"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "UPDATE pictures SET (picture_name = %s, picture_alt_text = %s, picture_path = %s) WHERE picture_id = %s",
                    (pic_name, pic_alt_text, pic_path, pic_id),
                )
                ret = cur.rowcount
        return ret
