from reactpy import html
from reactpy.backend.flask import Options

head = (
    html.title('Testing app'),
    html.link({
        "rel": "stylesheet",
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
        "integrity": "sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9",
        "crossorigin": "anonymous",
    }),
    html.link({
        "rel": "stylesheet",
        "href": "/static/dark.css",
    }),
)

g_options = Options(head=head)
