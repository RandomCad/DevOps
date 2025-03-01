use std::{path::PathBuf, io};

use rocket::{delete, fs::{FileServer, TempFile}, launch, put, routes, State};

static FILE_PATH: &str = "./files";

#[put("/<path..>", data = "<file>")]
async fn set_file(path: PathBuf, mut file: TempFile<'_>, base: &State<PathBuf>) -> io::Result<()> {
    file.persist_to(base.join(path)).await
}

#[delete("/<path..>")]
fn delete_file(path: PathBuf, base: &State<PathBuf>) -> io::Result<()> {
    std::fs::remove_file(base.join(path))
}

#[launch]
fn rocket() -> _ {
    let base = PathBuf::from(FILE_PATH).canonicalize().expect("should be valid");
    rocket::build()
        .mount("/", routes![set_file, delete_file])
        .mount("/", FileServer::from(base.clone()))
        .manage(base)
}