mkdir -p files
rm -f files/__test.txt

kind=$1

if [[ $kind = "docker" ]]; then
    docker run -d -p 8000:8000 --name hamster_test hamster:test
else
    target/debug/hamster &
    pid=$!
fi

sleep 1

assert() {
    if [[ $1 != $2 ]]; then
        echo "assertion failed: $1 != $2"
        finish 1
    fi
}

finish() {
    if [[ $kind = "docker" ]]; then
        docker stop hamster_test -t 3
    else
        kill $pid
    fi
    exit $1
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

finish 0