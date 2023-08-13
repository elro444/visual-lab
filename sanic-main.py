#!/usr/bin/env python3

from sanic import Sanic

from reactpy.backend.sanic import configure

from visual_lab import Base
from options import g_options
from fetch_data import fetch_data_periodic

app = Sanic("MyApp")
configure(app, Base, options=g_options)
app.static("/static", "./static")
app.add_task(fetch_data_periodic())

if __name__ == '__main__':
    app.run(host="0.0.0.0")  # Run the ASGI app


