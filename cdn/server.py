#!/usr/bin/env python
import urllib.parse
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from functools import partial
import socketserver

import termcolor

green = partial(termcolor.colored, color='green', attrs=('bold',))
yellow = partial(termcolor.colored, color='yellow', attrs=('bold',))
blue = partial(termcolor.colored, color='blue', attrs=('bold',))
red = partial(termcolor.colored, color='red', attrs=('bold',))

# STATIC_FILES = [
#     '/@material-ui/core@4.12.4'
# ]


class CachingHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        cdn_url = "https://cdn.jsdelivr.net" + self.path
        filename = urllib.parse.quote(cdn_url, safe="")
        filepath = os.path.abspath(os.path.join("static", filename))

        if not filepath.startswith(os.path.abspath("static")):
            self.send_response(403)
            self.end_headers()
            return

        if not os.path.exists(filepath):
            print(yellow(f'Caching file {self.path!r}'))
            try:
                response = urllib.request.urlopen(cdn_url)
            except Exception:
                print(red(f'Failed to cache file {self.path}'))
                self.send_response(404)
                return

            content = response.read()
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(content)
        else:
            print(green(f'Using cached file {filepath!r}'))

        if os.path.exists(filepath):
            self.send_response(200)
            self.send_header(
                "Access-Control-Allow-Origin",
                "http://localhost:8000"
            )
            self.send_header("Content-Type", "text/javascript")
            self.end_headers()
            with open(filepath, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


def run(port):
    os.chdir(os.path.dirname(__file__))
    server_address = ('', port)
    with ThreadingHTTPServer(server_address, CachingHTTPRequestHandler) as server:
        server.serve_forever()


if __name__ == '__main__':
    run(port=9999)
