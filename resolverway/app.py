#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import inspect

from flask import Flask

from views import bp

def create_app(config=None):
    """
    Create the application and return it to the user
    :return: flask.Flask application
    """

    app = Flask(__name__, static_folder=None)
    app.url_map.strict_slashes = False

    app.register_blueprint(bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
