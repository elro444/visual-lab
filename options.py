from reactpy import html
from reactpy.backend.flask import configure, Options

head = (
    html.title('Testing app'),
    html.link({
        "rel": "stylesheet",
        "href": "/static/dark.css",
    })
)

g_options = Options(head=head)
