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
    #[test]
    fn md() {
        let html = markdown::to_html("## Hello, *world*!");
        assert_eq!(html, "<h2>Hello, <em>world</em>!</h2>");
    }
}
