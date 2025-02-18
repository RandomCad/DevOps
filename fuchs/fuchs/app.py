"""defining the API endpoints for the notes application"""
from fastapi import FastAPI
from markdown import markdown
import requests

from . import db_connection, URL_HAMSTER


app = FastAPI()


@app.get("/notes/{note_id}")
def read_note(note_id: int):
    """returns the markdown content of a note"""
    note_content_md = db_connection.read_note(note_id)
    return {"id": note_id, "content": note_content_md}


@app.post("/notes/")
def create_note(note_content_md: str):
    """creates a new note.\n
    takes the markdown content of the note as input, converts it to html and
    stores the markdown in the db and distributes the html over the hamster.\n
    returns the path to the note for the hamster"""
    # TODO implement a way to integrate pictures (also in put & delete)
    # convert to html
    note_content_html = markdown(note_content_md)

    # safe the markdown
    note_id = db_connection.write_note(note_content_md)

    note_path = f"note_{note_id}"
    url = f"{URL_HAMSTER}/{note_path}"
    # safe the html on the hamster
    r = requests.put(url, data=note_content_html, timeout=10)

    assert r.status_code == 200
    assert note_path == r.json()["path"]

    return {"status": "created", "id": note_id, "path": note_path}


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_content_md: str):
    """updates the content of a note.\n
    takes the new markdown content of the note as input, converts it to html,
    updates the old markdown (on db) and html (on hamster).\n"""
    # convert to html
    note_content_html = markdown(note_content_md)

    # safe the markdown
    affected_rows = db_connection.update_note(note_id, note_content_md)
    assert affected_rows == 1

    note_path = f"note_{note_id}"
    url = f"{URL_HAMSTER}/{note_path}"
    # safe the html on the hamster
    r = requests.put(url, data=note_content_html, timeout=10)

    assert r.status_code == 200
    assert note_path == r.json()["path"]

    return {"status": "updated", "id": note_id}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    """deletes a note.\n
    removes both the markdown (db) and the html content (hamster)."""
    # delete the markdown
    affected_rows = db_connection.remove_note(note_id)
    assert affected_rows == 1

    note_path = f"note_{note_id}"
    url = f"{URL_HAMSTER}/{note_path}"
    # delete the html on the hamster
    r = requests.delete(url, timeout=10)
    assert r.status_code == 200
    assert note_path == r.json()["path"]

    return {"status": "deleted"}


@app.post("/pics/")
def store_picture(content_pic: str):
    """stores a picture on the hamster.\n
    returns the path to the picture."""
    # TODO store pic on hamster and return filepath
    return {"status": "created", "path": "/pics/dummy.png"}


@app.put("/pics/{pic_path}")
def update_picture(pic_path: str, content_pic: str):
    """updates a picture on the hamster.\n
    takes the new picture content as input and updates the picture on the
    hamster."""
    # TODO validate pic exists and update pic
    return {"status": "updated", "path": pic_path}


@app.delete("/pics/{pic_path}")
def delete_pic(pic_path: int):
    """deletes a picture on the hamster."""
    # TODO delete pic
    return {"status": "deleted"}
