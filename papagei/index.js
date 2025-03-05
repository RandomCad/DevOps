/*
tbd:
    note anzeigen:
        get_note_by_id

    note navigator updaten mit daten von api:
        get_all_note_navigator


    onclick_note_navigator

    open_note

    edit
    save_node

    delete_note_main -> tell api to delete note with note_id
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

function get_all_note_navigator() {
    // get json from api with all note ids and titles
    return get_example_all_note_navigator();
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
    open_note(0, 'Neue Notiz', 'Hier ist Platz für Ihre Ideen und Gedanken', 'Lollo');
}

function open_note(note_id, title, date, content, author) {
    show_note_title(title);
    show_note_author(date)
    show_note_author(author);
    show_note_content(content);
    set_note_main_id(note_id);
}

function show_note_title(title) {
    var note_title = document.getElementsByClassName("note_main_title")[0];
    note_title.innerHTML = title;
}
function show_note_date(date) {
    var note_date = document.getElementsByClassName("note_main_date")[0];
    note_date.innerHTML = date;
}
function show_note_author(author) {
    var note_author = document.getElementsByClassName("note_main_author")[0];
    note_author.innerHTML = author;
}
function show_note_content(content) {
    var note_content = document.getElementsByClassName("note_main_content")[0];
    note_content.innerHTML = content;
}

function get_note_by_id(note_id) {
    // tbd get note from api with note_id
    return get_example_note()
    .then(data => {
        return data;
    });
}

function open_note_by_id(note_id) {
    get_note_by_id(note_id)
        .then(data => {
            open_note(data.id,
                data.title,
                data.date,
                data.content,
                data.author);
        });
}




function open_note_on_start() {
    var note_navigator = document.getElementsByClassName("note_navigator")[0];
    if (note_navigator) {
        open_note_by_id(note_navigator.getAttribute("note_id"));
    }
    else {
        create_new_note();
    }
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
        // tell api to delete note with note_id
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


// example functions

function get_example_note() {
    return fetch("examples/example.json")
        .then(response => {
            if (!response.ok) {
                throw new Error("Fehler beim Öffnen der exaple.json");
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
