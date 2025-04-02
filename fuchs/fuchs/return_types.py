from typing import Literal
from pydantic import BaseModel, Field


class ClientErrorResponse(BaseModel):
    detail: str = Field(
        examples=["Invalid request: Missing title"],
        description="Error message describing the issue",
    )

class ServerErrorResponse(BaseModel):
    detail: str = Field(
        examples=["Server error: Database connection failed"],
        description="Error message describing the issue",
    )

ERROR_RESPONSES = {
    400: {
        "description": "Invalid Request",
        "model": ClientErrorResponse,
    },
    500: {
        "description": "Server Error",
        "model": ServerErrorResponse,
    },
}


class NoteResponse(BaseModel):
    class MediaResponse(BaseModel):
        id: int = Field(examples=[1], description="ID of the media file")
        path: str = Field(
            examples=["note_1/media/1"],
            description="Path to the media file on the hamster server",
            title="Media Path",
        )

    id: int = Field(
        examples=[1],
        description="ID of the note",
        title="Note ID",
    )
    title: str = Field(
        examples=["My first note"],
        description="Title of the note",
        title="Note Title",
    )
    content: str = Field(
        examples=["# My first note\n\nThis is my first note."],
        description="Markdown content of the note",
        title="Note Content",
    )
    path: str = Field(
        examples=["note_1/web.html"],
        description="Path to the note on the hamster server",
        title="Note Path",
    )
    media: list[MediaResponse]


class NotesResponse(BaseModel):
    class ReducedNoteResponse(BaseModel):
        id: int = Field(examples=[1], description="ID of the note")
        title: str = Field(
            examples=["My first note"],
            description="Title of the note",
        )

    notes: list[ReducedNoteResponse] = Field(
        examples=[
            [
                {"id": 1, "title": "My first note"},
                {"id": 2, "title": "My second note"},
            ]
        ],
        description="List of reduced note objects",
    )


class CreateResponse(BaseModel):
    status: Literal["created"] = Field(
        examples=["created"], description="Status of the creation operation"
    )
    id: int = Field(
        examples=[1], description="ID of the newly created resource"
    )
    path: str = Field(
        examples=["note_1/web.html"],
        description="Path to the newly created resource",
    )


class UpdateResponse(BaseModel):
    status: Literal["updated"] = Field(
        examples=["updated"], description="Status of the update operation"
    )
    id: int = Field(examples=[1], description="ID of the updated resource")


class DeleteResponse(BaseModel):
    status: Literal["deleted"] = Field(
        examples=["deleted"], description="Status of the delete operation"
    )
