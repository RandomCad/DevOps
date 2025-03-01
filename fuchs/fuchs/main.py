"""defining the API endpoints for the notes application"""

from fastapi import FastAPI, Depends
import requests

from . import (
    URL_HAMSTER,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
)  # , URL_CHAMELEON
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
    pic_data = db.read_all_meta_of_pictures(note_id)
    pics = [{"id": pic[0], "name": pic[1], "alt_text": pic[2]} for pic in pic_data]
    return {"id": note_id, "content": note_content_md, "pictures": pics}


@app.post("/notes/")
def create_note(
    note_title: str, note_content_md: str, db: DatabaseConnection = Depends(get_db)
):
    """creates a new note.\n
    takes the markdown content of the note as input, converts it to html and
    stores the markdown in the db and distributes the html over the hamster.\n
    returns the path to the note for the hamster"""
    # TODO implement a way to auto integrate pictures in the markdown
    # (atm the papagei has to first upload the picture and then integrate it in
    # the markdown, which isn't clean)

    # convert to html
    note_content_html = convert_md_to_html(note_content_md)

    # safe the markdown
    note_id = db.write_note(note_title, note_content_md)

    note_path = f"note_{note_id}"
    url = f"{URL_HAMSTER}/{note_path}"
    # safe the html on the hamster
    r = requests.put(url, data=note_content_html, timeout=10)

    assert r.status_code == 200

    # safe the path to the note in the db
    affected_rows = db.update_note(note_id, note_title, note_content_md, note_path)
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

    note_path = f"note_{note_id}"
    # safe the markdown
    affected_rows = db.update_note(note_id, note_title, note_content_md, note_path)
    assert affected_rows == 1, f"affected_rows: {affected_rows}"

    note_path = f"note_{note_id}"
    url = f"{URL_HAMSTER}/{note_path}"
    # safe the html on the hamster
    r = requests.put(url, data=note_content_html, timeout=10)

    assert r.status_code == 200

    return {"status": "updated", "id": note_id}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: DatabaseConnection = Depends(get_db)):
    """deletes a note.\n
    removes both the markdown (db) and the html content (hamster)."""
    # delete the markdown
    affected_rows = db.remove_note(note_id)
    assert affected_rows == 1

    note_path = f"note_{note_id}"
    url = f"{URL_HAMSTER}/{note_path}"
    # delete the html on the hamster
    r = requests.delete(url, timeout=10)
    assert r.status_code == 200

    return {"status": "deleted"}


@app.post("/notes/{note_id}/pics/")
def store_picture(
    note_id: int,
    pic_content: str,
    pic_name: str,
    pic_alt_text: str,
    db: DatabaseConnection = Depends(get_db),
):
    """stores a picture on the hamster.\n
    returns the path to the picture."""
    # TODO: get rid of multiple implementation of note_path- & pic_path-generation
    pic_path = f"note_{note_id}/pics/{pic_name}"
    url = f"{URL_HAMSTER}/{pic_path}"
    r = requests.put(url, data=pic_content, timeout=10)
    assert r.status_code == 200

    pic_id = db.store_meta_of_picture(note_id, pic_name, pic_alt_text, pic_path)

    return {"status": "created", "id": pic_id, "path": pic_path}


@app.put("/notes/{note_id}/pics/{pic_id}")
def update_picture(
    note_id: int,
    pic_id: int,
    pic_content: str,
    pic_name: str,
    pic_alt_text: str,
    db: DatabaseConnection = Depends(get_db),
):
    """updates a picture on the hamster.\n
    takes the new picture content as input and updates the picture on the
    hamster."""
    # TODO: get rid of multiple implementation of note_path- & pic_path-generation
    pic_path = f"note_{note_id}/pics/{pic_name}"
    url = f"{URL_HAMSTER}/{pic_path}"
    r = requests.put(url, data=pic_content, timeout=10)
    assert r.status_code == 200

    affected_rows = db.update_meta_of_picture(pic_id, pic_name, pic_alt_text, pic_path)
    assert affected_rows == 1

    return {"status": "updated", "path": pic_path}


@app.delete("/notes/{note_id}/pics/{pic_id}")
def delete_pic(pic_id: int, pic_path: str, db: DatabaseConnection = Depends(get_db)):
    """deletes a picture and its metadata."""
    affected_rows = db.remove_meta_of_picture(pic_id)
    assert affected_rows == 1

    url = f"{URL_HAMSTER}/{pic_path}"
    r = requests.delete(url, timeout=10)
    assert r.status_code == 200

    return {"status": "deleted"}


def convert_md_to_html(md: str) -> str:
    """converts markdown to html"""
    # r = requests.post(f"http://{URL_CHAMELEON}/", data=md, timeout=10)
    # assert r.status_code == 200
    # return r.text
    return md
