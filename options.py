from reactpy import html
from reactpy.backend.flask import Options

head = (
    html.title('Testing app'),
    html.link({
        "rel": "stylesheet",
        "href": "http://localhost:9999/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
        # "integrity": "sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9",
        # "crossorigin": "anonymous",
    }),
    html.script({
        'src': 'http://localhost:9999/npm/jquery@3.2.1/dist/jquery.min.js',
        # "crossorigin": "anonymous",
    }),
    html.script({
        'src': 'http://localhost:9999/npm/popper.js@1.12.9/dist/umd/popper.min.js'
    }),
    html.script({
        "src": "http://localhost:9999/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js",
        # "integrity": "sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm",
        # "crossorigin": "anonymous",
    }),
    # html.script({
    #     'src': 'http://localhost:9999/npm/requirejs@2.3.6/require.min.js',
    #     # 'crossorigin': 'anonymous',
    # }),
    # html.script({
    #     'src': 'http://localhost:9999/npm/react@18.2.0/umd/react.production.min.js',
    #     # 'crossorigin': 'anonymous',
    # }),
    # html.script({
    #     'src': 'http://localhost:9999/npm/react-dom@18.2.0/index.min.js',
    #     # 'crossorigin': 'anonymous',
    # }),
    html.link({
        "rel": "stylesheet",
        "href": "/static/dark.css",
    }),
)

g_options = Options(head=head)
