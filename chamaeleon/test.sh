# setup
kind=$1
if [[ $kind = "docker" ]]; then
    docker run -d --rm -p 8000:8000 --name chamaeleon_test chamaeleon:test
else
    target/debug/chamaeleon &
    pid=$!
fi

sleep 1

finish() {
    if [[ $kind = "docker" ]]; then
        docker stop chamaeleon_test -t 3
    else
        kill $pid
    fi
}

exec_test() {
    converted=$( \
    curl -X POST http://localhost:8000 \
        -s -H "Content-Type: text/plain" \
        --data-binary "@chamaeleon/test_data/inp_$1.txt" \
    | sed "s/^[[:blank:]]*//;s/[[:blank:]]*$//")
    expected=$(cat "chamaeleon/test_data/out_$1.txt" | sed "s/^[[:blank:]]*//;s/[[:blank:]]*$//")
    if [[ $converted != $expected ]]; then
        echo -e "expected:\n$expected"
        echo -e "got:\n$converted"
        finish
        exit 1
    fi
}

exec_test basic
exec_test table

finish
exit 0
