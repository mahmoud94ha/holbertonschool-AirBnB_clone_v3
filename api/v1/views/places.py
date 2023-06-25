#!/usr/bin/python3
"""
Contains the api app.py
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def retrieves_all_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if "user_id" not in place_data.keys():
        abort(400, "Missing user_id")

    user = storage.get(User, place_data.get("user_id"))
    if not user:
        abort(404)

    if "name" not in place_data.keys():
        abort(400, "Missing name")

    place_data["city_id"] = city_id
    place = Place(**place_data)
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place_data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    elif not place_data:
        abort(400, "Not a JSON")

    for key, value in place_data.items():
        ignored_keys = ["id", "state_id", "city_id",
                        "created_at", "updated_at"]
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=['POST'],
                 strict_slashes=False)
def place_search():
    """Retrieves all Place objects depending of the JSON"""
    list_obj = []
    obj_request = request.get_json()
    if obj_request:
        if "states" in obj_request and len(obj_request["states"]) > 0:
            list_states = obj_request["states"]
            for state_id in list_states:
                state = storage.get("State", state_id)
                if state:
                    list_cities = state.cities
                    for city in list_cities:
                        list_places = city.places
                        for place in list_places:
                            list_obj.append(place.to_dict())

        if "cities" in obj_request and len(obj_request["cities"]) > 0:
            list_cities = obj_request["cities"]
            for city_id in list_cities:
                city = storage.get("City", city_id)
                if city:
                    list_places = city.places
                    for place in list_places:
                        list_obj.append(place.to_dict())
        return jsonify(list_obj)
