import webbrowser

import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from socket import socket
from urllib.parse import urlparse, parse_qs


# HTTP handler for processing the token sent from the web browser
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        params = parse_qs(url.query)
        token = params.get("token", [""])[0]

        if token:
            self.respond(200, "OK")
            self.server.token = token
        else:
            self.respond(400, "Bad Request")

        self.server._stop()

    # Suppress logging
    def log_message(self, format, *args):
        pass

    # Format the response
    def respond(self, code, message):
        self.send_response(code)
        self.send_header("Content-type", "text")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Origin, X-Requested-With, Content-Type, Accept",
        )
        self.end_headers()
        self.wfile.write(message.encode("utf8"))


# Temporary HTTP server to handle the login process
class Server(HTTPServer):
    port = None
    token = None
    thread = None

    def __init__(self, app_domain: str):
        sock = socket()
        sock.bind(("", 0))
        self.port = sock.getsockname()[1]
        super().__init__(("localhost", self.port), Handler)

        self.app_domain = app_domain

    def get_token(self):
        self._start()
        self._open_browser()

        while self.thread is not None:
            time.sleep(1)

        return self.token

    def _open_browser(self):
        webbrowser.open(f"{self.app_domain}/signup?cli={self.port}")

    def _start(self):
        thread = Thread(target=self.serve_forever)
        thread.start()
        self.thread = thread

    def _stop(self):
        Thread(target=self.shutdown).start()
        self.thread = None
