#!/usr/bin/python3
"""
Contains the api app.py
"""
from api import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """get status"""
    return jsonify({"status": "OK"})
