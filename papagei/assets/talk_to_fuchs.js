"use strict"

export async function get_notes() {
    return fetch('/notes')
    .then(response => {
        if (!response.ok) {
            throw new Error("Fehler beim Abfragen aller Notes");
        }
        return response.json();
    })
    .then(data => {
        return data.notes;
    })
    .catch(error => {
        console.error('Fehler:', error);
        return false;
    });
}

export async function get_note_by_id(note_id) {
    return fetch('/notes/' + note_id)
    .then(response => {
        if (!response.ok) {
            throw new Error("Fehler beim Abfragen von Note mit ID: " + note_id);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        return data;
    })
    .catch(error => {
        console.error('Fehler:', error);
        return false;
    });
}

export async function update_note_by_id(note_id, note_title, note_content_md) {
    return new Promise(function (resolve, reject) {
        fetch(`/notes/${note_id}?note_title=${encodeURIComponent(note_title)}&note_content_md=${encodeURIComponent(note_content_md)}`, {
            method: "PUT",
            headers: {
                "accept": "application/json"
            }
        })
        .then(response => {
            if (response.ok) {
                console.log("Updaten Erfolgreich", response);
                resolve(true);
            }
            else {
                console.error(`Fehler beim Updaten der Notiz mit Title: ${note_title} ${response.status} ${response.statusText}`);
                reject(false);
            }
        });
    });
}

export async function delete_note_by_id(note_id) {
    return new Promise(function (resolve, reject) {
        fetch("/notes/" + note_id, {
            method: "DELETE"
        })
        .then(response => {
            if (response.ok) {
                console.log("Löschen Erfolgreich:", response);
                resolve(true);
            }
            else {
                console.error(`Fehler beim Löschen von Note mit ID: ${note_id} ${response.status} ${response.statusText}`);
                reject(false)
            }
        });
    });
}

export async function create_note(note_title, note_content_md) {
    return new Promise(function (resolve, reject) {
        fetch(`/notes/?note_title=${encodeURIComponent(note_title)}&note_content_md=${encodeURIComponent(note_content_md)}`, {
            method: "POST",
            headers: {
                "accept": "application/json"
            }
        })
        .then(response => {
            if (response.ok) {
                console.log("Erstellen Erfolgreich", response);
                resolve(true);
            }
            else {
                console.error(`Fehler beim Erstellen der Notiz mit Title: ${note_title} ${response.status} ${response.statusText}`);
                reject(false);
            }
        });
    });
}

export function store_media(note_id, file) {
    
}

export function update_media(note_id, media_id, file) {
    
}

export function delete_media(note_id, media_id) {

}
