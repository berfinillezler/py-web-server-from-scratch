# Python Web Server from Scratch 

A tiny HTTP/1.1 static-file server written with only the Python standard library.  
It serves files from `./static`, handles multiple clients via threads, logs each request and shuts down cleanly on Ctrl+C.

## Features
- Raw TCP sockets (`socket`) — no frameworks
- `GET` for static assets (HTML/CSS/JS/images)
- Correct `Content-Type` via `mimetypes`
- Multithreading (one thread per connection)
- Structured logging with timestamps & thread names
- Graceful shutdown on `KeyboardInterrupt`

## How it works (quick tour)
1. Bind a TCP socket and `listen()` on `HOST:PORT`.
2. For each client, a thread runs `handle_client(conn)`.
3. Parse the request line: `GET /path HTTP/1.1`.
4. Map the path to `./static/<file>` safely.
5. Send headers + file bytes or `404` if missing.

## Project structure
```
web-server/
├─ server.py
└─ static/
   ├─ index.html
   ├─ style.css
   ├─ script.js
   └─ image.png
```

## Requirements
- Python 3.10+

## Run
```bash
python3 server.py
# → Server running at http://127.0.0.1:8080/
```

Now open http://127.0.0.1:8080/ in your browser.

## Notes & Limitations
- Only `GET` is implemented (no POST/PUT/DELETE).
- No HTTPS/TLS, HTTP/2, compression, or keep-alive.
- One thread per connection (no thread pooling).
- Minimal security hardening (e.g., basic path checks only).
- Intended for learning/demo purposes, not production.