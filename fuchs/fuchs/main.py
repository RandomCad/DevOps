"""defining the API endpoints for the notes application"""

import requests

from fastapi import FastAPI, Depends, UploadFile

from . import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    URL_HAMSTER,
    URL_CHAMAELEON,
)
from .database import DatabaseConnection


app = FastAPI()


def get_db():
    """returns a database connection"""
    db = DatabaseConnection(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
    )
    try:
        yield db
    finally:
        db.conn.close()


@app.get("/notes")
def read_all_notes(db: DatabaseConnection = Depends(get_db)):
    """returns a list of all notes"""
    notes = db.read_all_notes()
    ret = {"notes": [{"id": note[0], "title": note[1]} for note in notes]}
    return ret


@app.get("/notes/{note_id}")
def read_note(note_id: int, db: DatabaseConnection = Depends(get_db)):
    """returns the markdown content of a note plus the metadata of pictures
    of the note"""
    note_content_md = db.read_note(note_id)
    media_data = db.read_all_meta_of_media(note_id)
    media = [{"id": pic[0], "path": pic[1]} for pic in media_data]
    return {"id": note_id, "content": note_content_md, "pictures": media}


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

    # convert to html
    note_content_html = convert_md_to_html(note_content_md)

    # safe the markdown
    note_id = db.write_note(note_title, note_content_md)

    note_path = f"note_{note_id}/web.html"
    url = f"{URL_HAMSTER}/{note_path}"
    # safe the html on the hamster
    r = requests.put(url, data=note_content_html, timeout=10)

    assert r.status_code == 200, r.text

    # safe the path to the note in the db
    affected_rows = db.update_note(
        note_id, note_title, note_content_md, note_path
    )
    assert affected_rows == 1, f"affected_rows: {affected_rows}"

    return {"status": "created", "id": note_id, "path": note_path}


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
    # convert to html
    note_content_html = convert_md_to_html(note_content_md)

    note_path = f"note_{note_id}/web.html"
    # safe the markdown
    affected_rows = db.update_note(
        note_id, note_title, note_content_md, note_path
    )
    assert affected_rows == 1, f"affected_rows: {affected_rows}"

    url = f"{URL_HAMSTER}/{note_path}"
    # safe the html on the hamster
    r = requests.put(url, data=note_content_html, timeout=10)

    assert r.status_code == 200, f"status: {r.status_code}\nmessage: {r.text}"

    return {"status": "updated", "id": note_id}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: DatabaseConnection = Depends(get_db)):
    """deletes a note.\n
    removes both the markdown (db) and the html content (hamster)."""
    # delete the markdown
    affected_rows = db.remove_note(note_id)
    assert affected_rows == 1

    note_path = f"note_{note_id}/web.html"
    url = f"{URL_HAMSTER}/{note_path}"
    # delete the html on the hamster
    r = requests.delete(url, timeout=10)
    assert r.status_code == 200

    return {"status": "deleted"}


@app.post("/notes/{note_id}/media/")
def store_media(
    note_id: int,
    file: UploadFile,
    db: DatabaseConnection = Depends(get_db),
):
    """stores a picture on the hamster.\n
    returns the path to the picture."""

    # create a new db entry to get an id
    media_id = db.store_meta_of_media(note_id, file.filename)

    # safe the picture on the hamster
    media_path = f"note_{note_id}/media/{media_id}"
    url = f"{URL_HAMSTER}/{media_path}"
    files = {"file": (file.filename, file.file, file.content_type)}
    r = requests.put(url, files=files, timeout=10)
    assert r.status_code == 200, (
        f"status_code: {r.status_code},\n answer: {r.text}, \n url: {url}"
    )

    # update metadata
    # insert the path of the picture in the db
    affected_rows = db.update_meta_of_media(media_id, file.filename, media_path)
    assert affected_rows == 1

    return {"status": "created", "id": media_id, "path": media_path}


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
    media_path = f"note_{note_id}/media/{media_id}"
    url = f"{URL_HAMSTER}/{media_path}"
    files = {"file": (file.filename, file.file, file.content_type)}
    r = requests.put(url, files=files, timeout=10)
    assert r.status_code == 200

    affected_rows = db.update_meta_of_media(media_id, file.filename, media_path)
    assert affected_rows == 1

    return {"status": "updated", "path": media_path}


@app.delete("/notes/{note_id}/media/{media_id}")
def delete_pic(media_id: int, db: DatabaseConnection = Depends(get_db)):
    """deletes a picture and its metadata."""
    # Get the path of the picture
    media_data = db.read_meta_of_media(media_id)
    media_path = media_data[2]

    affected_rows = db.remove_meta_of_media(media_id)
    assert affected_rows == 1

    url = f"{URL_HAMSTER}/{media_path}"
    r = requests.delete(url, timeout=10)
    assert r.status_code == 200

    return {"status": "deleted"}


def convert_md_to_html(md: str) -> str:
    """converts markdown to html"""
    r = requests.post(f"{URL_CHAMAELEON}/", data=md, timeout=10)
    assert r.status_code == 200
    return r.text
