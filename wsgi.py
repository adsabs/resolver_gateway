# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    entrypoint wsgi script
"""

from werkzeug.serving import run_simple
from resolverway import app

application = app.create_app()

if __name__ == "__main__":
    run_simple('0.0.0.0', 5050, application, use_reloader=True, use_debugger=True)
