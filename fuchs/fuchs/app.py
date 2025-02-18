"""defining the API endpoints for the notes application"""
from fastapi import FastAPI


app = FastAPI()


@app.get("/notes/{note_id}")
def read_note(note_id: int):
    """returns the markdown content of a note"""
    # TODO get note
    return {"id": note_id, "title": "note Title", "content": "note Content"}


@app.post("/notes/")
def create_note(content_markdown: str):
    """creates a new note.\n
    takes the markdown content of the note as input, converts it to html and
    stores the markdown in the db and distributes the html over the hamster.\n
    returns the path to the note for the hamster"""
    note_id = 1 # TODO get dynamic id

    # TODO convert markdown to html and store both (markdown -> db, html -> hamster)
    note_path = "/notes/dummy.html"
    return {"status": "created", "id": note_id, "path": note_path}


@app.put("/notes/{note_id}")
def update_note(note_id: int, content_markdown: str):
    """updates the content of a note.\n
    takes the new markdown content of the note as input, converts it to html,
    updates the old markdown (on db) and html (on hamster).\n"""
    # TODO update note
    return {"status": "updated", "id": note_id}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    """deletes a note.\n
    removes both the markdown (db) and the html content (hamster)."""
    # TODO validate note exists? and delete note
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
