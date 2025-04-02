/*
tbd:

    api:
        get_note_by_id
        get_all_note_navigator
        delete_note

        save: give data to api
            needs papagei-save

    
    papagei:
        edit: open a edit mode
        upload images and events
        save: extrakt data von note

        open_note: images, html, markdown ????


    extra:
        change background between default backgrounds
        date in note_navigator

*/

// note navigator
"use strict";

function create_note_navigator(note_id, title) {
    var div = document.createElement("div");
    var div_bg = document.createElement("div");
    div.innerHTML = title;
    // div_bg.setAttribute('note_id', note_id);
    div_bg.addEventListener("click", function() {
        onclick_note_navigator(note_id);
    });
    div_bg.classList.add("note_navigator_bgdiv");
    div.classList.add("note_navigator");

    var style = getComputedStyle(document.documentElement);
    var parent_div = document.querySelector(".note_navigator_box");
    if (parent_div) {
        parent_div.appendChild(div_bg);
        div_bg.appendChild(div);
    }
    else {
        console.error('create_note_navigator: no element with class "note_navigator_box" found');
    }
}

function update_all_note_navigator() {
    document.querySelectorAll(".note_navigator_bgdiv").forEach(element => element.remove());
    get_all_note_navigator()
        .then(data=>{
            console.log(data);
            for (const index in data) {
                var note = data[index];
                console.log(note);
                create_note_navigator(note.id, note.title);
            }
        })
}

function onclick_note_navigator(note_id) {
    console.log(" on click note navigator " + note_id);
    open_note_by_id(note_id)
}



// note main

function create_new_note() {
    console.log("Create new note");
    check_if_note_needs_to_be_saved();
    let now = new Date();
    get_neue_notiz_note()
    .then(data => {
        open_note({note_id: data.id,
            title: data.title,
            date: now.toISOString(),
            author: data.author,
            content: data.content,
            link: data.link
        });
    });

    //open_note(0, 'Neue Notiz', now.toISOString(), 'Hier ist Platz für Ihre Ideen und Gedanken', 'Lollo');
}

function open_note({note_id, title, date, author, content, link}) {
    set_note_main_id(note_id);
    show_note_title(title);
    show_note_date(date)
    show_note_author(author);
    show_note_content({content: content, link: link});
}

function show_note_title(title) {
    var note_title = document.getElementsByClassName("note_main_title")[0];
    note_title.innerHTML = title;
}
function show_note_date(date_str) {
    /**
     * @param {string} date_str - ISO 8601-format "2025-03-07T20:50:07.232Z"
     */
    var note_date = document.getElementsByClassName("note_main_date")[0];
    const date = new Date(date_str);
    const formattedDateTime = date.toLocaleString('de-DE');
    
    note_date.textContent = formattedDateTime;
    note_date.setAttribute("datetime", date_str);
}
function show_note_author(author) {
    var note_author = document.getElementsByClassName("note_main_author")[0];
    note_author.innerHTML = author;
}
function show_note_content({content, link}) {
    var note_content = document.getElementsByClassName("note_main_content")[0];
    var note_content_iframe = document.getElementsByClassName("note_main_content_iframe")[0];
    if (link) {
        note_content_iframe.setAttribute("src", HAMSTER_BASE_URL + "/" + link);
        note_content.innerHTML = "";
        note_content.style.display = "none";
        note_content_iframe.style.display = "block";
    }
    else {
        note_content.innerHTML = content;
        note_content_iframe.setAttribute("src", "about:blank");
        note_content.style.display = "block";
        note_content_iframe.style.display = "none";
    }
}

function open_note_by_id(note_id) {
    get_note_by_id(note_id)
        .then(data => {
            console.log(data);
            open_note({
                note_id: data.id,
                title: data.title,
                date: data.date,
                author: data.author,
                content: data.content,
                link: data.path
            });
        });
}




function open_note_on_start() {
    /*
    var note_navigator = document.getElementsByClassName("note_navigator")[0];
    if (note_navigator) {
        open_note_by_id(note_navigator.getAttribute("note_id"));
    }
    else {
        create_new_note();
    }
    */
    create_new_note();
}

function check_if_note_needs_to_be_saved(params) {
    if (check_note_main_edit_mode == true) {
        if (confirm("Es gibt ungespeicherte Änderungen.\nSoll die Notiz gespeichert werden)")) {
            save_node();
        }
    }
    // note wird nicht editiert und muss entsprechend nicht gespeichert werden
}

function save_node() {
    
}

function set_note_main_edit_mode() {
    var note_main = document.getElementsByClassName("note_main")[0];
    if (!note_main) {
        console.error('set_note_main_id: no element with class "note_main" found');
        show_error_and_reload();
    }
    else {
        note_main.setAttribute("edit", true);
    }
}

function clear_note_main_edit_mode() {
    var note_main = document.getElementsByClassName("note_main")[0];
    if (!note_main) {
        console.error('set_note_main_id: no element with class "note_main" found');
        show_error_and_reload();
    }
    else {
        note_main.removeAttribute("edit");
    }
}

function check_note_main_edit_mode() {
    var note_main = document.getElementsByClassName("note_main")[0];
    if (!note_main) {
        console.error('set_note_main_id: no element with class "note_main" found');
        show_error_and_reload();
    }
    else {
        if (note_main.getAttribute("edit") == true) {
            return true;
        }
        else {
            return false;
        }
    }
}

function set_note_main_id(note_id) {
    var note_main = document.getElementsByClassName("note_main")[0];
    if (!note_main) {
        console.error('set_note_main_id: no element with class "note_main" found');
        show_error_and_reload();
    }
    else {
        note_main.setAttribute("note_id", note_id);
    }
}

function get_note_main_id() {
    var note_main = document.getElementsByClassName("note_main")[0];
    if (!note_main) {
        console.error('get_note_main_id: no element with class "note_main" found');
        show_error_and_reload();
    }
    else {
        var note_id = note_main.getAttribute("note_id");
        if (!note_id) {
        console.error('get_note_main_id: element with class "note_main" has no attribute "note_id"');
        show_error_and_reload();
        } 
        else {
            return note_id;
        }
    }
}

function clear_note_main_id() {
    var note_main = document.getElementsByClassName("note_main")[0];
    if (!note_main) {
        console.error('clear_note_main_id: no element with class "note_main" found');
        show_error_and_reload();
    }
    else {
        note_main.removeAttribute("note_id");
    }
}

function delete_note() {
    var note_id = get_note_main_id();
    if (note_id) {
        delete_note_by_id(note_id)
        clear_note_main_id();
        clear_note_main_edit_mode();
        create_new_note();
        update_all_note_navigator();
    }
}

function show_error_and_reload(message = "Ein Fehler ist aufgetreten! Seite neu laden?") {
    if (confirm(message)) {
        location.reload();
    }
}

function get_time_and_day() {
    
}


// communicate with fuchs

function get_all_note_navigator() {
    // get json from api with all note ids and titles
  
    return fetch('/notes')
        .then(response => {
            if (!response.ok) {
                throw new Error("Fehler beim Abfragen aller Notes");
            }
            return response.json(); // Antwort als JSON parsen
        })
        .then(data => {
            return data.notes;
        }) // Daten verwenden
        .catch(error => {
            console.error('Fehler:', error);
        });

    // return get_example_all_note_navigator();
}

function get_note_by_id(note_id) {
    return fetch('/notes/' + note_id)
        .then(response => {
            if (!response.ok) {
                throw new Error("Fehler beim Abfragen von Note mit ID: " + note_id);
            }
            return response.json(); // Antwort als JSON parsen
        })
        .then(data => {
            console.log(data);
            return data;
        }) // Daten verwenden
        .catch(error => {
            console.error('Fehler:', error);
        });

    // return get_example_note()
    // .then(data => {
    //     return data;
    // });
}

function delete_note_by_id(note_id) {
    console.log(`Delete Note with ID: ${note_id}`);
    fetch("/notes/" + note_id, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Fehler beim Löschen von Note mit ID: ${note_id} ${response.status} ${response.statusText}`);
            }
            console.log(response);
            response.json();
        })
        .then(data => console.log('Löschen Erfolgreich:', data))
        .catch(error => console.error('Fehler2:', error));
      
    // fetch('http://127.0.0.1:8000/notes/0', {
    //     method: 'DELETE',
    //     headers: {
    //       'Accept': 'application/json'
    //     }
    //   })
    //   .then(response => {
    //     if (!response.ok) {
    //       throw new Error(`Fehler: ${response.status} ${response.statusText}`);
    //     }
    //     return response.json().catch(() => ({})); // Falls keine JSON-Antwort kommt
    //   })
    //   .then(data => console.log('Löschen erfolgreich:', data))
    //   .catch(error => console.error('Fehler:', error));
      
}


// example functions

function get_example_note() {
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

function get_neue_notiz_note() {
    return fetch("assets/neue_notiz.json")
    .then(response => {
        if (!response.ok) {
            throw new Error("Fehler beim Öffnen von neue_notiz.json");
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

function get_example_all_note_navigator() {
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


// old functions

function test_create_note_navigator(n) {
    for (let index = 1; index <= n; index++) {
        create_note_navigator(index, 'Note '+index);

    }
}
