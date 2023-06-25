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


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def places_search():
    """places_search"""
    search_data = request.get_json()
    if not search_data:
        abort(400, "Not a JSON")

    states = search_data.get("states", [])
    cities = search_data.get("cities", [])
    amenities = search_data.get("amenities", [])

    places = storage.all(Place).values()

    if states or cities:
        filtered_places = []
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    filtered_places.extend(state.places)
        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    filtered_places.extend(city.places)

        places = set(places).intersection(filtered_places)

    if amenities:
        filtered_places = []
        for place in places:
            if all(amenity_id in place.amenities for amenity_id in amenities):
                filtered_places.append(place)
        places = filtered_places

    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)
