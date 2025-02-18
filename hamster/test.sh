mkdir -p files
rm -f files/__test.txt

target/debug/hamster &
pid=$!

sleep 1

assert() {
    if [[ $1 != $2 ]]; then
        echo "assertion failed: $1 != $2"
        kill $pid
        exit 1
    fi
}

curl_status() {
    if [[ $2 != "" ]]; then
        curl -s -o /dev/null -X $1 localhost:8000/__test.txt -w "%{http_code}" -H "Content-Type: text/plain" -d "$2"
    else
        curl -s -o /dev/null -X $1 localhost:8000/__test.txt -w "%{http_code}"
    fi
}

assert 404 $(curl_status GET)
assert 200 $(curl_status PUT "hamster")
assert 200 $(curl_status GET)
assert "hamster" $(curl -s localhost:8000/__test.txt)
assert 200 $(curl_status PUT "hamster2")
assert "hamster2" $(curl -s localhost:8000/__test.txt)
assert 200 $(curl_status DELETE)
assert 500 $(curl_status DELETE)
assert 404 $(curl_status GET)

kill $pid
exit 0