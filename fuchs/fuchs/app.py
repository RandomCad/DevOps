"""defining the API endpoints for the notes application"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/notes/{note_id}")
def read_note(note_id: int):
    # TODO get note
    return {"id": note_id, "title": "note Title", "content": "note Content"}


@app.post("/notes/")
def create_note():
    # TODO generate new id
    note_id = 1
    return {"status": "created", "id": note_id}


@app.put("/notes/{note_id}")
def update_note(note_id: int):
    # TODO update note
    return {"status": "updated", "id": note_id}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    # TODO delete note
    return {"status": "deleted", "id": note_id}
