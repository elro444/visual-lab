#!/usr/bin/env python
from flask import Flask

from reactpy import html
from reactpy.backend.flask import configure, Options

from visual_lab import Base



app = Flask(__name__)

head = (
    html.title('Testing app'),
    html.link({
        "rel": "stylesheet",
        "href": "/static/dark.css",
    })
)

configure(app, Base, options=Options(head=head))
app.run('0.0.0.0', 8000, debug=True, )
