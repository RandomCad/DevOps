/*
tbd:
    save_note should return note_id
    cursor button
    delete when in edit mode
    alles was mit medien zu tun hat
        upload 
        send to api

    extra:
        change background between default backgrounds
        date in note_navigator

*/

// note navigator
"use strict";

import * as fuchs from "./talk_to_fuchs.js";
import * as example_functions from "./examples/example_functions.js";

document.addEventListener("DOMContentLoaded", async () => {
    var note_main = document.getElementsByClassName("note_main_body")[0];
    console.log(note_main);
    document.getElementsByClassName("note_create_button")[0]
        .addEventListener("click", create_new_note);
    document.getElementsByClassName("note_main_delete")[0]
        .addEventListener("click", delete_note);
    document.getElementsByClassName("note_main_edit")[0]
        .addEventListener("click", toggle_edit_mode);
    // document.getElementsByClassName("note_main_save")[0]
    //     .addEventListener("click", save_note);
    // example_functions.create_example_note_with_md();
    await update_all_note_navigator();
    open_note_on_start();
});

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

async function update_all_note_navigator() {
    document.querySelectorAll(".note_navigator_bgdiv").forEach(element => element.remove());
    const note_navigators = await fuchs.get_notes();
    
    // .then(data=>{
    //         if (data === false) {
    //             // Fehler beim Abfragen aller note_navigators
    //             show_error_and_reload("Fehler beim Abfragen aller Notizen")
    //         }
    //         else {
    for (const index in note_navigators) {
        var note = note_navigators[index];
        create_note_navigator(note.id, note.title);
    }
        //     }
        // })
}

function onclick_note_navigator(note_id) {
    console.log(" on click note navigator " + note_id);
    open_note_by_id(note_id);
}



// note main

function create_new_note() {
    console.log("Create new note");
    check_if_note_needs_to_be_saved();
    //let now = new Date();
    show_note_main_content();
    get_neue_notiz_note()
    .then(data => {
        open_note({note_id: null,
            title: data.title,
            //date: now.toISOString(),
            //author: data.author,
            content: data.content,
            link: data.link
        });
    });
}

function open_note({note_id, title, content, link}) {
    // {note_id, title, date, author, content, link}
    set_note_main_id(note_id);
    show_note_title(title);
    //show_note_date(date)
    //show_note_author(author);
    show_note_content({content: content, link: link});
}

function show_note_title(title) {
    const note_title = document.getElementsByClassName("note_main_title")[0];
    note_title.innerHTML = title;
}

function get_note_title() {
    const note_title = document.getElementsByClassName("note_main_title")[0];
    if (note_title) {
        return note_title.textContent;
    }
    else {
        console.log('get_note_title:: kein Element mit class "note_main_title" gefunden');
        return null;
    }
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
        note_content_iframe.setAttribute("src", "/" + link);
        note_content.innerHTML = "";
        show_note_main_content_iframe();
    }
    else {
        note_content.innerHTML = content;
        note_content_iframe.setAttribute("src", "about:blank");
        show_note_main_content();
    }
}

function show_note_main_content() {
    var note_main_content = document.getElementsByClassName("note_main_content")[0];
    var note_main_content_iframe = document.getElementsByClassName("note_main_content_iframe")[0];
    var textarea_markdown = document.getElementsByClassName("textarea_markdown")[0];
    if (note_main_content && note_main_content_iframe && textarea_markdown) {
        note_main_content.style.display = "block";
        note_main_content_iframe.style.display = "none";
        textarea_markdown.style.display = "none";
    }
    else {
        console.error("note_main_content or note_main_content_iframe or textarea_markdown not found");
        show_error_and_reload();
    }
}

function show_note_main_content_iframe() {
        var note_main_content = document.getElementsByClassName("note_main_content")[0];
        var note_main_content_iframe = document.getElementsByClassName("note_main_content_iframe")[0];
        var textarea_markdown = document.getElementsByClassName("textarea_markdown")[0];
        if (note_main_content && note_main_content_iframe && textarea_markdown) {
            note_main_content.style.display = "none";
            note_main_content_iframe.style.display = "block";
            textarea_markdown.style.display = "none";
        }
        else {
            console.error("note_main_content or note_main_content_iframe or textarea_markdown not found");
            show_error_and_reload();
        }
}

function show_textarea_markdown(focus = false) {
    var note_main_content = document.getElementsByClassName("note_main_content")[0];
    var note_main_content_iframe = document.getElementsByClassName("note_main_content_iframe")[0];
    var textarea_markdown = document.getElementsByClassName("textarea_markdown")[0];
    if (note_main_content && note_main_content_iframe && textarea_markdown) {
        note_main_content.style.display = "none";
        note_main_content_iframe.style.display = "none";
        textarea_markdown.style.display = "block";
        if (focus) {
            textarea_markdown.focus();
        }
    }
    else {
        console.error("note_main_content or note_main_content_iframe or textarea_markdown not found");
        show_error_and_reload();
    }
}

function get_note_content() {
    const textarea_markdown = document.getElementsByClassName("textarea_markdown")[0];
    if (textarea_markdown) {
        return textarea_markdown.value;
    }
    else {
        console.log('get_note_content:: kein Element mit class "textarea_markdown" gefunden');
        return null;
    }
}

function open_note_by_id(note_id) {
    fuchs.get_note_by_id(note_id)
        .then(data => {
            if (data === false) {
                // Fehler beim Abfragen der Note
                show_error_and_reload("Fehler: Notiz konnte nicht geöffnet werden!");
            }
            else {
                console.log(data);
                open_note({
                    note_id: data.id,
                    title: data.title,
                    //date: data.date,
                    //author: data.author,
                    content: data.content,
                    link: data.path
                });
            }
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

async function check_if_note_needs_to_be_saved() {
    if (check_note_main_edit_mode() === true) {
        if (confirm("Es gibt ungespeicherte Änderungen.\nSoll die Notiz gespeichert werden)")) {
            console.log(`check_if_note_needs_to_be_saved:: confirmed`)
            const note_id = await save_note();
            return note_id;
        }
        else {
            console.log(`check_if_note_needs_to_be_saved:: canceld`)
            return get_note_main_id();
        }
    }
    // note wird nicht editiert und muss entsprechend nicht gespeichert werden
}

async function save_note() {
    console.log(`save_note:: start`)
    if (check_note_main_edit_mode() === true) {
        let note_id = get_note_main_id();
        const note_title = get_note_title();
        const note_content_md = get_note_content();
        if (!note_title) {
            note_title = "Notiz";
        }
        if (!note_content_md) {
            note_content_md = "";
        }
        if (note_id === null) {
            // neue Note
            console.log(`save_note:: erstelle neue Notiz mit title: ${note_title}, content: ${note_content_md}`);
            const response = await fuchs.create_note(note_title, note_content_md);
            if (response === false) {
                show_error_and_reload("Fehler beim Erstellen einer neuen Notiz");
            }
            else {
                note_id = true;
                console.log("got response")
            }
        }
        else {
            // update Note
            console.log(`save_note:: aktualisiere Notiz mit id ${note_id} und title: ${note_title}, content: ${note_content_md}`);
            const response = await fuchs.update_note_by_id(note_id, note_title, note_content_md);
            if (response === false) {
                show_error_and_reload("Fehler beim Updaten einer Notiz");
            }
        }
        console.log("mach weiter")
        if (note_id && note_id !== true) {
            return note_id;
        }
        else {
            return null;
        }
    }
    return false;
}

function enable_save_button() {
    var save_button = document.getElementsByClassName("note_main_save")[0];
    if (save_button) {
        save_button.disable = false;
    }
    else {
        console.log('enable_save_button: kein element mit class "note_main_save"');
        show_error_and_reload();
    }
}

function disable_save_button() {
    var save_button = document.getElementsByClassName("note_main_save")[0];
    if (save_button) {
        save_button.disable = true;
    }
    else {
        console.log('disable_save_button: kein element mit class "note_main_save"');
        show_error_and_reload();
    }
}

async function toggle_edit_mode() {
    if (check_note_main_edit_mode() === false) {
        // start edit mode
        set_note_main_edit_mode();
        toggle_note_title_edit_mode(true);
        var note_main_title = document.getElementsByClassName("note_main_title")[0];
        show_textarea_markdown(true);
        var textarea_markdown = document.getElementsByClassName("textarea_markdown")[0];
        var note_id = get_note_main_id();
        if (note_id === null) {
            // neue Notiz
            get_neue_notiz_note()
            .then(data => {
                textarea_markdown.value = data.content;
                note_main_title.textContent = data.title;
            });
        }
        else {
            // note anzeigen
            fuchs.get_note_by_id(note_id)
            .then(data => {
                if (data === false) {
                    // Fehler beim Abfragen der Note
                    show_error_and_reload("Fehler: Notiz konnte nicht geöffnet werden!");
                }
                else {
                    textarea_markdown.value = data.content;
                    note_main_title.textContent = data.title;
                }
            });
        }
    }
    else {
        // end edit mode
        var note_id = await check_if_note_needs_to_be_saved();
        clear_note_main_edit_mode();
        toggle_note_title_edit_mode(false);
        update_all_note_navigator();
        console.log(note_id);
        if (note_id === false) {
            // do nothing
        }
        else if (note_id === null) {
            create_new_note();
        }
        else {
            open_note_by_id(note_id);
        }
    }
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
        if (note_main.getAttribute("edit")) {
            return true;
        }
        else {
            return false;
        }
    }
}

function toggle_note_title_edit_mode(edit = false) {
    var note_main_title = document.getElementsByClassName("note_main_title")[0];
    if (note_main_title) {
        note_main_title.contentEditable = edit;
    }
    else {
        console.error('set_note_main_edit_mode: no element with class "note_main_title" found');
        show_error_and_reload();
    }
}

function set_note_main_id(note_id) {
    if (note_id === null) {
        clear_note_main_id();
    }
    else {
        var note_main = document.getElementsByClassName("note_main")[0];
        if (!note_main) {
            console.error('set_note_main_id: no element with class "note_main" found');
            show_error_and_reload();
        }
        else {
            note_main.setAttribute("note_id", note_id);
        }
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
        if (note_id) {
            return note_id;
        }
        else {
            return null
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

async function delete_note() {
    var note_id = get_note_main_id();
    if (note_id !== null) {
        const result = await fuchs.delete_note_by_id(note_id);
        if (result === true) {
            console.log("Note gelöscht", result);
            clear_note_main_id();
            clear_note_main_edit_mode();
            create_new_note();
            update_all_note_navigator();
        }
        else {
            show_error_and_reload("Fehler beim Löschen der Notiz");
        };
    }
    else {
        clear_note_main_id();
        clear_note_main_edit_mode();
        create_new_note();
        update_all_note_navigator();
    }
}

function show_error_and_reload(message = "Ein Fehler ist aufgetreten! Seite neu laden?", reload = true ) {
    if (confirm(message)) {
        if (reload === true) {
            location.reload();
        }
    }
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