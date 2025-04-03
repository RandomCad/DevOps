const HTML_PREFIX: &str = r#"<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="assets/note.css">
</head>
<body>
"#;
const HTML_SUFFIX: &str = "
</body>
</html>";

#[rocket::post("/", data = "<body>")]
fn convert(body: String) -> String {
    HTML_PREFIX.to_string()
        + &markdown::to_html_with_options(&body, &markdown::Options::gfm())
            .expect("only mdx can err")
        + HTML_SUFFIX
}

#[rocket::launch]
fn rocket() -> _ {
    rocket::build().mount("/", rocket::routes![convert])
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn basic() {
        let html = convert("## Hello, *world*!".to_string());let expected = r#"<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="assets/note.css">
</head>
<body>
<h2>Hello, <em>world</em>!</h2>
</body>
</html>"#;
        assert_eq!(html, expected);
    }

    #[test]
    fn table() {
        let md = "| col1 | col2 |
| --- | --- |
| abc | def |";
        let html = super::convert(md.to_string());
        let expected = r#"<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="assets/note.css">
</head>
<body>
<table>
<thead>
<tr>
<th>col1</th>
<th>col2</th>
</tr>
</thead>
<tbody>
<tr>
<td>abc</td>
<td>def</td>
</tr>
</tbody>
</table>
</body>
</html>"#;
        assert_eq!(html, expected);
    }
}
