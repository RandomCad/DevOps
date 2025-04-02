"""defining the API endpoints for the notes application"""

import logging
from typing import NoReturn

from fastapi import FastAPI, Depends, UploadFile, HTTPException

from .helpers import (
    put_file_on_hamster,
    delete_file_on_hamster,
    convert_md_to_html,
)
from .database import DatabaseConnection, get_db
from .return_types import (
    ERROR_RESPONSES,
    CreateResponse,
    UpdateResponse,
    DeleteResponse,
    NoteResponse,
    NotesResponse,
)

logger = logging.getLogger("uvicorn.error")

NOTE_PATH = "note_{note_id}/web.html"
MEDIA_PATH = "note_{note_id}/media/{media_id}"

app = FastAPI()


def raise_errors(result: dict) -> None | NoReturn:
    """raises an HTTPException if the result of an operation is an error"""
    if result["status"] == "error":
        logger.error(result)
        (code, kind) = (
            (500, "Server error")
            if result.get("type") == "server"
            else (400, "Invalid request")
        )
        raise HTTPException(
            status_code=code, detail=f"{kind}: {result['message']}"
        )


def test_not_empty(**kwargs: str) -> None | NoReturn:
    """raises an HTTPException if any of the input values are empty"""
    for key, val in kwargs.items():
        if not val:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid request: Empty input {key}",
            )


@app.get("/notes", tags=["notes"], responses={**ERROR_RESPONSES})
def read_all_notes(db: DatabaseConnection = Depends(get_db)) -> NotesResponse:
    """returns a list of all notes"""
    result = db.read_all_notes()
    raise_errors(result)
    return {
        "notes": [{"id": note[0], "title": note[1]} for note in result["data"]]
    }


@app.get("/notes/{note_id}", tags=["notes"], responses={**ERROR_RESPONSES})
def read_note(
    note_id: int, db: DatabaseConnection = Depends(get_db)
) -> NoteResponse:
    """returns the markdown content of a note plus the metadata of pictures
    of the note"""
    result = db.read_note(note_id)
    raise_errors(result)
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
        "media": media,
    }


@app.post("/notes/", tags=["notes"], responses={**ERROR_RESPONSES})
def create_note(
    note_title: str,
    note_content_md: str,
    db: DatabaseConnection = Depends(get_db),
) -> CreateResponse:
    """creates a new note.\n
    takes the markdown content of the note as input, converts it to html and
    stores the markdown in the db and distributes the html over the hamster.\n
    returns the path to the note for the hamster"""
    test_not_empty(note_title=note_title, note_content_md=note_content_md)

    result = db.write_note(note_title, note_content_md)
    raise_errors(result)
    note_id = result["data"]

    result = convert_md_to_html(note_content_md)
    raise_errors(result)
    note_content_html = result["html"]

    note_path = NOTE_PATH.format(note_id=note_id)
    result = put_file_on_hamster(note_path, note_content_html)
    raise_errors(result)

    result = db.update_note(note_id, note_title, note_content_md, note_path)
    raise_errors(result)

    return {"status": "created", "id": note_id, "path": note_path}


@app.put("/notes/{note_id}", tags=["notes"], responses={**ERROR_RESPONSES})
def update_note(
    note_id: int,
    note_title: str,
    note_content_md: str,
    db: DatabaseConnection = Depends(get_db),
) -> UpdateResponse:
    """updates the content & title of a note.\n
    takes the new markdown content of the note as input, converts it to html,
    updates the old markdown (on db) and html (on hamster).\n"""
    test_not_empty(note_title=note_title, note_content_md=note_content_md)
    result = db.read_note(note_id)
    raise_errors(result)
    note_path = result["data"][2]

    result = convert_md_to_html(note_content_md)
    raise_errors(result)
    note_content_html = result["html"]

    result = put_file_on_hamster(note_path, note_content_html)
    raise_errors(result)

    result = db.update_note(note_id, note_title, note_content_md, note_path)
    raise_errors(result)

    return {"status": "updated", "id": note_id}


@app.delete("/notes/{note_id}", tags=["notes"], responses={**ERROR_RESPONSES})
def delete_note(
    note_id: int, db: DatabaseConnection = Depends(get_db)
) -> DeleteResponse:
    """deletes a note.\n
    removes both the markdown (db) and the html content (hamster)."""
    result = db.read_note(note_id)
    raise_errors(result)
    note_path = result["data"][2]

    result = delete_file_on_hamster(note_path)
    raise_errors(result)

    result = db.remove_note(note_id)
    raise_errors(result)

    return {"status": "deleted"}


@app.post(
    "/notes/{note_id}/media/",
    tags=["media"],
    responses={**ERROR_RESPONSES},
)
def store_media(
    note_id: int,
    file: UploadFile,
    db: DatabaseConnection = Depends(get_db),
) -> CreateResponse:
    """stores a picture on the hamster.\n
    returns the path to the picture."""
    result = db.store_meta_of_media(note_id, file.filename)
    raise_errors(result)
    media_id = result["data"]

    media_path = MEDIA_PATH.format(note_id=note_id, media_id=media_id)
    result = put_file_on_hamster(media_path, file.file)
    raise_errors(result)

    result = db.update_meta_of_media(media_id, file.filename, media_path)
    raise_errors(result)

    return {"status": "created", "id": media_id, "path": media_path}


@app.put(
    "/notes/{note_id}/media/{media_id}",
    tags=["media"],
    responses={**ERROR_RESPONSES},
)
def update_media(
    note_id: int,
    media_id: int,
    file: UploadFile,
    db: DatabaseConnection = Depends(get_db),
) -> UpdateResponse:
    """updates a picture on the hamster.\n
    takes the new picture content as input and updates the picture on the
    hamster."""
    result = db.read_meta_of_media(media_id)
    raise_errors(result)
    if result["data"][0] != note_id:
        result["status"] = "error"
        result["type"] = "client"
        result["message"] = "Media not found"
        raise_errors(result)
    media_path = result["data"][2]

    result = put_file_on_hamster(media_path, file.file)
    raise_errors(result)

    result = db.update_meta_of_media(media_id, file.filename, media_path)
    raise_errors(result)

    return {"status": "updated", "id": media_id}


@app.delete(
    "/notes/{note_id}/media/{media_id}",
    tags=["media"],
    responses={**ERROR_RESPONSES},
)
def delete_media(
    note_id: int, media_id: int, db: DatabaseConnection = Depends(get_db)
) -> DeleteResponse:
    """deletes a media file and its metadata."""
    result = db.read_meta_of_media(media_id)
    raise_errors(result)
    if result["data"][0] != note_id:
        result["status"] = "error"
        result["type"] = "client"
        result["message"] = "Media not found"
        raise_errors(result)
    media_path = result["data"][2]

    result = delete_file_on_hamster(media_path)
    raise_errors(result)

    result = db.remove_meta_of_media(media_id)
    raise_errors(result)

    return {"status": "deleted"}
