// example functions

import * as fuchs from "../talk_to_fuchs.js";

export function get_example_note() {
    return fetch("examples/example.json")
        .then(response => {
            if (!response.ok) {
                throw new Error("Fehler beim Öffnen von exaple.json");
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error("Error: ", error)
        })
}

export function get_example_all_note_navigator() {
    return fetch("examples/example_all_note_navigator.json")
    .then(response => {
        if (!response.ok) {
            throw new Error("Fehler beim Öffnen der example_all_note_navigator.json");
        }
        return response.json();
    })
    .then(data => {
        return data.note_navigators;
    })
    .catch(error => {
        console.error("Error: ", error)
    })
}

export function create_example_note_with_md() {
    fuchs.create_note("Test", 
        `# Test

## Inhaltsverzeichnis
- [Alalala](#alalala)
- [Kuchen](#kuchen)

## Alalala
- Tiger  
- Delfin  
- Papagei  

## Kuchen
| Kuchen        | Hauptzutat     |
|--------------|--------------|
| Apfelkuchen  | Äpfel        |
| Schokokuchen | Schokolade   |
| Käsekuchen   | Quark        |
`
    );
}



// old functions

export function test_create_note_navigator(n) {
    for (let index = 1; index <= n; index++) {
        create_note_navigator(index, 'Note '+index);

    }
}