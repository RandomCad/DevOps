mkdir -p files
rm -f files/__test.txt
rm -rf files/__long

kind=$1

if [[ $kind = "docker" ]]; then
    docker run -d --rm -p 8000:8000 --name hamster_test -v ./files:/app/files hamster:test
else
    target/debug/hamster &
    pid=$!
fi

sleep 1

assert() {
    if [[ $1 != $2 ]]; then
        echo "assertion failed: $1 != $2"
        finish
        exit 1
    fi
}

finish() {
    if [[ $kind = "docker" ]]; then
        docker stop hamster_test -t 3
    else
        kill $pid
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
assert 200 $(curl -s -o /dev/null -X PUT localhost:8000/__long/path/to/file.txt -w "%{http_code}" -H "Content-Type: text/plain" -d "test3")
assert 200 $(curl -s -o /dev/null -X PUT localhost:8000/__long/path/to/file2.txt -w "%{http_code}" -H "Content-Type: text/plain" -d "test4")

finish

if [[ $(cat files/__long/path/to/file.txt) != "test3" ]]; then
    echo "file vanished"
    exit 1
fi

exit 0