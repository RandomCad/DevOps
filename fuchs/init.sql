CREATE TABLE IF NOT EXISTS notes (
    note_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    note_title TEXT NOT NULL,
    note_content TEXT NOT NULL,
    note_path TEXT
);

CREATE TABLE IF NOT EXISTS pictures (
    picture_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    note_id INT REFERENCES notes(note_id),
    picture_name TEXT NOT NULL,
    picture_alt_text TEXT NOT NULL,
    picture_path TEXT NOT NULL
)