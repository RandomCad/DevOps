"""defining the API endpoints for the notes application"""

from fastapi import FastAPI, Depends, UploadFile, HTTPException

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
    result = db.read_all_notes()
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid request. Please check your parameters.",
        )
    return {
        "notes": [{"id": note[0], "title": note[1]} for note in result["data"]]
    }


@app.get("/notes/{note_id}")
def read_note(note_id: int, db: DatabaseConnection = Depends(get_db)):
    """returns the markdown content of a note plus the metadata of pictures
    of the note"""
    result = db.read_note(note_id)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400, detail="Note not found. Please check the note ID."
        )
    (note_title, note_content_md, note_path) = result["data"]
    media_data = db.read_all_meta_of_media(note_id)
    if media_data["status"] == "error":
        return media_data
    media = [{"id": m[0], "path": m[1]} for m in media_data["data"]]
    return {
        "id": note_id,
        "title": note_title,
        "content": note_content_md,
        "path": note_path,
        "pictures": media,
    }


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
    result = db.write_note(note_title, note_content_md)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide valid note details.",
        )
    note_id = result["data"]

    result = convert_md_to_html(note_content_md)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide valid note details.",
        )
    note_content_html = result["html"]

    note_path = NOTE_PATH.format(note_id=note_id)
    result = put_file_on_hamster(note_path, note_content_html)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide valid note details.",
        )

    result = db.update_note(note_id, note_title, note_content_md, note_path)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide valid note details.",
        )

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
    result = db.read_note(note_id)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide valid note details.",
        )
    note_path = result["data"][2]

    result = convert_md_to_html(note_content_md)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide valid note details.",
        )
    note_content_html = result["html"]

    result = put_file_on_hamster(note_path, note_content_html)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide valid note details.",
        )

    result = db.update_note(note_id, note_title, note_content_md, note_path)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide valid note details.",
        )

    return {"status": "updated", "id": note_id}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: DatabaseConnection = Depends(get_db)):
    """deletes a note.\n
    removes both the markdown (db) and the html content (hamster)."""
    result = db.read_note(note_id)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400, detail="Note not found. Please check the note ID."
        )
    note_path = result["data"][2]

    result = delete_file_on_hamster(note_path)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400, detail="Note not found. Please check the note ID."
        )

    result = db.remove_note(note_id)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400, detail="Note not found. Please check the note ID."
        )

    return {"status": "deleted"}


@app.post("/notes/{note_id}/media/")
def store_media(
    note_id: int,
    file: UploadFile,
    db: DatabaseConnection = Depends(get_db),
):
    """stores a picture on the hamster.\n
    returns the path to the picture."""
    result = db.store_meta_of_media(note_id, file.filename)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide a valid media file.",
        )
    media_id = result["data"]

    media_path = MEDIA_PATH.format(note_id=note_id, media_id=media_id)
    result = put_file_on_hamster(media_path, file.file)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide a valid media file.",
        )

    result = db.update_meta_of_media(media_id, file.filename, media_path)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide a valid media file.",
        )

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
    result = db.read_meta_of_media(media_id)
    if result["status"] == "error" or result["data"][0] != note_id:
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide a valid media file.",
        )
    media_path = result["data"][2]

    result = put_file_on_hamster(media_path, file.file)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide a valid media file.",
        )

    result = db.update_meta_of_media(media_id, file.filename, media_path)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide a valid media file.",
        )

    return {"status": "updated", "path": media_path}


@app.delete("/notes/{note_id}/media/{media_id}")
def delete_media(
    note_id: int, media_id: int, db: DatabaseConnection = Depends(get_db)
):
    """deletes a media file and its metadata."""
    result = db.read_meta_of_media(media_id)
    if result["status"] == "error" or result["data"][0] != note_id:
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Media not found. Please check the media ID.",
        )
    media_path = result["data"][2]

    result = delete_file_on_hamster(media_path)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Media not found. Please check the media ID.",
        )

    result = db.remove_meta_of_media(media_id)
    if result["status"] == "error":
        if result.get("type") == "server":
            raise HTTPException(status_code=500, detail="Server error occurred")
        raise HTTPException(
            status_code=400,
            detail="Media not found. Please check the media ID.",
        )

    return {"status": "deleted"}
