"""defining the API endpoints for the notes application"""

from fastapi import FastAPI, Depends, UploadFile

from .helpers import (
    put_file_on_hamster,
    delete_file_on_hamster,
    convert_md_to_html,
)
from .database import DatabaseConnection, get_db


NOTE_PATH = "note_{note_id}/web.html"
MEDIA_PATH = "note_{note_id}/media/{media_id}"

app = FastAPI()


@app.get("/notes")
def read_all_notes(db: DatabaseConnection = Depends(get_db)):
    """returns a list of all notes, containing the id and title of each note"""
    try:
        notes = db.read_all_notes()
        assert notes is not None, "Failed to fetch notes"
        return {"notes": [{"id": note[0], "title": note[1]} for note in notes]}
    except AssertionError as e:
        return {"status": "error", "message": str(e)}
    except Exception:
        return {"status": "error", "message": "Internal Server Error"}


@app.get("/notes/{note_id}")
def read_note(note_id: int, db: DatabaseConnection = Depends(get_db)):
    """returns the markdown content of a note plus the metadata of pictures
    of the note"""
    try:
        # get the note content
        note_data = db.read_note(note_id)
        assert note_data is not None, f"Note with id {note_id} not found"
        (note_title, note_content_md, note_path) = note_data
        # get the media data
        media_data = db.read_all_meta_of_media(note_id)
        media = [{"id": m[0], "path": m[1]} for m in media_data]
        return {
            "id": note_id,
            "title": note_title,
            "content": note_content_md,
            "path": note_path,
            "pictures": media,
        }
    except AssertionError as e:
        return {"status": "error", "message": str(e)}
    except Exception:
        return {"status": "error", "message": "Internal Server Error"}


@app.post("/notes/")
def create_note(
    note_title: str,
    note_content_md: str,
    db: DatabaseConnection = Depends(get_db),
):
    """creates a new note.\n
    takes the markdown content of the note as input, converts it to html and
    stores the markdown in the db and distributes the html over the hamster.\n
    returns the path to the note for the hamster"""
    try:
        # safe the markdown, get an id
        note_id = db.write_note(note_title, note_content_md)
        assert note_id is not None, "Failed to create note"

        # convert to html
        note_content_html = convert_md_to_html(note_content_md)

        # generate a path for the note
        note_path = NOTE_PATH.format(note_id=note_id)
        # safe the html on the hamster
        put_file_on_hamster(note_path, note_content_html)

        # safe the path to the note in the db
        affected_rows = db.update_note(
            note_id, note_title, note_content_md, note_path
        )
        assert affected_rows == 1, "Failed to update metadata"

        return {"status": "created", "id": note_id, "path": note_path}
    except AssertionError as e:
        return {"status": "error", "message": str(e)}
    except Exception:
        return {"status": "error", "message": "Internal Server Error"}


@app.put("/notes/{note_id}")
def update_note(
    note_id: int,
    note_title: str,
    note_content_md: str,
    db: DatabaseConnection = Depends(get_db),
):
    """updates the content & title of a note.\n
    takes the new markdown content of the note as input, converts it to html,
    updates the old markdown (on db) and html (on hamster).\n"""
    try:
        # get the path of the note
        note_data = db.read_note(note_id)
        assert note_data is not None, f"Note with id {note_id} not found"
        note_path = note_data[2]

        # convert to html
        note_content_html = convert_md_to_html(note_content_md)

        # update the html on the hamster
        put_file_on_hamster(note_path, note_content_html)

        # update the markdown
        affected_rows = db.update_note(
            note_id, note_title, note_content_md, note_path
        )
        assert affected_rows == 1, "Failed to update metadata"

        return {"status": "updated", "id": note_id}
    except AssertionError as e:
        return {"status": "error", "message": str(e)}
    except Exception:
        return {"status": "error", "message": "Internal Server Error"}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: DatabaseConnection = Depends(get_db)):
    """deletes a note.\n
    removes both the markdown (db) and the html content (hamster)."""
    try:
        # get the path of the note
        note_data = db.read_note(note_id)
        assert note_data is not None, f"Note with id {note_id} not found"
        note_path = note_data[2]

        # delete the html on the hamster
        delete_file_on_hamster(note_path)

        # delete the markdown
        affected_rows = db.remove_note(note_id)
        assert affected_rows == 1, "Failed to delete metadata"

        return {"status": "deleted"}
    except AssertionError as e:
        return {"status": "error", "message": str(e)}
    except Exception:
        return {"status": "error", "message": "Internal Server Error"}


@app.post("/notes/{note_id}/media/")
def store_media(
    note_id: int,
    file: UploadFile,
    db: DatabaseConnection = Depends(get_db),
):
    """stores a picture on the hamster.\n
    returns the path to the picture."""
    try:
        # create a new db entry to get an id
        media_id = db.store_meta_of_media(note_id, file.filename)
        assert media_id is not None, "Failed to store media"

        # safe the picture on the hamster
        media_path = MEDIA_PATH.format(note_id=note_id, media_id=media_id)
        put_file_on_hamster(media_path, file.file)

        # update metadata
        # insert the path of the picture in the db
        affected_rows = db.update_meta_of_media(
            media_id, file.filename, media_path
        )
        assert affected_rows == 1, "Failed to update metadata"

        return {"status": "created", "id": media_id, "path": media_path}
    except AssertionError as e:
        return {"status": "error", "message": str(e)}
    except Exception:
        return {"status": "error", "message": "Internal Server Error"}


@app.put("/notes/{note_id}/media/{media_id}")
def update_media(
    note_id: int,
    media_id: int,
    file: UploadFile,
    db: DatabaseConnection = Depends(get_db),
):
    """updates a picture on the hamster.\n
    takes the new picture content as input and updates the picture on the
    hamster."""
    try:
        # Get the path of the picture
        media_data = db.read_meta_of_media(media_id)
        assert media_data is not None and media_data[0] == note_id, (
            f"Media with id {media_id} and note {note_id} not found"
        )
        media_path = media_data[2]

        # update the picture on the hamster
        put_file_on_hamster(media_path, file.file)

        # update metadata
        affected_rows = db.update_meta_of_media(
            media_id, file.filename, media_path
        )
        assert affected_rows == 1, "Failed to update metadata"

        return {"status": "updated", "path": media_path}

    except AssertionError as e:
        return {"status": "error", "message": str(e)}
    except Exception:
        return {"status": "error", "message": "Internal Server Error"}


@app.delete("/notes/{note_id}/media/{media_id}")
def delete_pic(
    note_id: int, media_id: int, db: DatabaseConnection = Depends(get_db)
):
    """deletes a picture and its metadata."""
    try:
        # Get the path of the picture
        media_data = db.read_meta_of_media(media_id)
        assert media_data is not None and media_data[0] == note_id, (
            f"Media with id {media_id} and note {note_id} not found"
        )
        media_path = media_data[2]

        # delete the picture on the hamster
        delete_file_on_hamster(media_path)

        # delete the metadata
        affected_rows = db.remove_meta_of_media(media_id)
        assert affected_rows == 1, "Failed to delete metadata"

        return {"status": "deleted"}
    except AssertionError as e:
        return {"status": "error", "message": str(e)}
    except Exception:
        return {"status": "error", "message": "Internal Server Error"}
