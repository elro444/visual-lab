#!/usr/bin/env python3

from sanic import Sanic

from reactpy.backend.sanic import configure

from visual_lab import Base

app = Sanic("MyApp")
configure(app, Base)

if __name__ == '__main__':
    app.run(host="0.0.0.0")  # Run the ASGI app


