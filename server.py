#!/usr/bin/env python3
"""
RideOps Support Intelligence Hub - Modern Web App Server
Zero extra dependencies required. Uses Python built-in standard library.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Concise logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

def run_server():
    port = PORT
    max_tries = 10
    httpd = None

    for attempt in range(max_tries):
        try:
            httpd = socketserver.TCPServer(("", port), Handler)
            break
        except OSError:
            port += 1

    if not httpd:
        print(f"Error: Could not bind to port {PORT}-{PORT + max_tries}")
        sys.exit(1)

    url = f"http://localhost:{port}"
    print("=" * 68)
    print(" 🚕  RideOps Support Intelligence Hub & Gatekeeper")
    print("=" * 68)
    print(f" Web app running at: {url}")
    print(f" Serving directory:  {DIRECTORY}")
    print(" You can also double-click 'index.html' to open directly in any browser.")
    print(" Press Ctrl+C to stop the server.")
    print("=" * 68)

    # Automatically open browser
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped. Goodbye!")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
