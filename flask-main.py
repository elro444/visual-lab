#!/usr/bin/env python
from flask import Flask

from options import g_options
from reactpy.backend.flask import configure

from visual_lab import VisualLab


app = Flask(__name__)

configure(app, VisualLab, options=g_options)
app.run('0.0.0.0', 8000, debug=True, )
