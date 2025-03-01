if [[ $1 = "docker" ]]; then
    docker run -d -p 8000:8000 --name chamaeleon_test chamaeleon:test
else
    target/debug/chamaeleon &
    pid=$!
fi

sleep 1

converted=$( \
curl -X POST http://localhost:8000 \
    -H "Content-Type: text/plain" \
    -d "## Hello *world*!")

if [[ $1 = "docker" ]]; then
    docker stop chamaeleon_test -t 3
else
    kill $pid
fi

if [[ $converted != "<h2>Hello <em>world</em>!</h2>" ]]; then
    exit 1
fi

exit 0
