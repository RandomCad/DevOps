target/debug/chamaeleon &
pid=$!
wait 1
converted=$( \
curl -X POST http://localhost:8000 \
    -H "Content-Type: text/plain" \
    -d "## Hello *world*!")
kill $pid

if [[ converted != "<h2>Hello, <em>world</em>!</h2>" ]]; then
    exit 1
fi