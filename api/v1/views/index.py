#!/usr/bin/python3
"""
Contains the api app.py
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flasgger import swag_from


@app_views.route('/status', methods=['GET'], strict_slashes=False)
@swag_from("../swaggerdocs/status/status.yml")
def get_status():
    """get status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
@swag_from("../swaggerdocs/stats/stats.yml")
def show_stats():
    """returns the count for all objects"""
    all_counts = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(all_counts)
