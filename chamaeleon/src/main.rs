#[rocket::post("/", data = "<body>")]
fn convert(body: String) -> String {
    markdown::to_html(&body)
}

#[rocket::launch]
fn rocket() -> _ {
    rocket::build().mount("/", rocket::routes![convert])
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn md() {
        let html = convert("## Hello, *world*!".to_string());
        assert_eq!(html, "<h2>Hello, <em>world</em>!</h2>");
    }
}
