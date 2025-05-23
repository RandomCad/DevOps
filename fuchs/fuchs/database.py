"""This module provides a class to connect to a PostgreSQL database and
provides methods to write, read and update notes"""

import psycopg2

from . import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
)


class DatabaseConnection:
    """connects to a PostgreSQL database and provides methods to write, read
    and update notes"""

    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host
        )

    def read_note(self, note_id: int):
        """reads a note from the database by id,
        returns a tuple with the title, content and path of the note"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "SELECT note_title, note_content, note_path FROM notes WHERE note_id = %s",
                        (note_id,),
                    )
                    ret = cur.fetchone()
            if ret is None:
                return {"status": "error", "message": "Note not found"}
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def read_all_notes(self):
        """reads all notes from the database,
        returns a list of tuples with the title and id of the notes"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute("SELECT note_id, note_title FROM notes")
                    ret = cur.fetchall()
            if ret is None:
                return {"status": "error", "message": "Failed to fetch notes"}
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def write_note(self, title: str, content: str, path: str = ""):
        """writes a new note to the database,
        returns the id of the new note"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO notes (note_title, note_content, note_path) VALUES (%s, %s, %s) RETURNING note_id",
                        (title, content, path),
                    )
                    ret = cur.fetchone()[0]
            if ret is None:
                return {"status": "error", "message": "Failed to create note"}
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def update_note(self, note_id: int, title: str, content: str, path: str):
        """updates a note in the database by id,
        returns the number of rows affected"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "UPDATE notes SET note_title = %s, note_content = %s, note_path = %s WHERE note_id = %s",
                        (title, content, path, note_id),
                    )
                    ret = cur.rowcount
            if ret != 1:
                return {
                    "status": "error",
                    "message": "Failed to update metadata",
                }
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def remove_note(self, note_id: int):
        """removes a note from the database by id,
        returns the number of rows affected"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM notes WHERE note_id = %s", (note_id,)
                    )
                    ret = cur.rowcount
            if ret != 1:
                return {
                    "status": "error",
                    "message": "Failed to delete metadata",
                }
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def read_meta_of_media(self, media_id: int):
        """reads the meta information of a media by id,
        returns a tuple with the note_id, name and alt_text of the media"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "SELECT note_id, media_name, media_path FROM media WHERE media_id = %s",
                        (media_id,),
                    )
                    ret = cur.fetchone()
            if ret is None:
                return {"status": "error", "message": "Media not found"}
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def read_all_meta_of_media(self, note_id: int):
        """reads all media of a note by id,\n
        returns a list of tuples with the id, name, alt_text and path of the
        media"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "SELECT media_id, media_name, media_path FROM media WHERE note_id = %s",
                        (note_id,),
                    )
                    ret = cur.fetchall()
            if ret is None:
                return {"status": "error", "message": "Failed to fetch media"}
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def store_meta_of_media(
        self, note_id: int, media_name: str, media_path: str = ""
    ):
        """stores the reference between a media and a note,
        returns the id of the media"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO media (note_id, media_name, media_path) VALUES (%s, %s, %s) RETURNING media_id",
                        (note_id, media_name, media_path),
                    )
                    ret = cur.fetchone()[0]
            if ret is None:
                return {"status": "error", "message": "Failed to store media"}
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def update_meta_of_media(
        self, media_id: int, media_name: str, media_path: str
    ):
        """updates the meta information of a media by id,
        returns the number of rows affected"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "UPDATE media SET media_name = %s, media_path = %s WHERE media_id = %s",
                        (media_name, media_path, media_id),
                    )
                    ret = cur.rowcount
            if ret != 1:
                return {
                    "status": "error",
                    "message": "Failed to update metadata",
                }
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }

    def remove_meta_of_media(self, media_id: int):
        """removes a media from the database by id,
        returns the number of rows affected"""
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM media WHERE media_id = %s", (media_id,)
                    )
                    ret = cur.rowcount
            if ret != 1:
                return {
                    "status": "error",
                    "message": "Failed to delete metadata",
                }
            return {"status": "success", "data": ret}
        except psycopg2.Error as e:
            return {
                "status": "error",
                "type": "server",
                "message": f"Database operation failed: {e}",
            }
        except Exception as e:
            return {
                "status": "error",
                "type": "user",
                "message": f"Invalid input: {e}",
            }


def get_db():
    """returns a database connection"""
    db = DatabaseConnection(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
    )
    try:
        yield db
    finally:
        db.conn.close()
