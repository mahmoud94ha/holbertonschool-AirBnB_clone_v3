#!/usr/bin/python3
"""
Contains the api app.py
"""
import os
from flask import Flask
from models import storage
from api import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """teardown_appcontext"""
    storage.close()

if __name__ == "__main__":
    """main"""
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
