CREATE TABLE IF NOT EXISTS notes (
    note_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    note_title TEXT NOT NULL,
    note_content TEXT NOT NULL,
    note_path TEXT
);

CREATE TABLE IF NOT EXISTS media (
    media_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    note_id INT REFERENCES notes(note_id),
    media_name TEXT NOT NULL,
    media_path TEXT NOT NULL
)