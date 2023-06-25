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
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
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
    place_data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    elif not place_data:
        abort(400, "Not a JSON")

    for key, value in place_data.items():
        ignored_keys = ["id", "state_id", "city_id", "created_at", "updated_at"]
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def places_search():
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")

    states = place_data.get("states", [])
    cities = place_data.get("cities", [])
    amenities = place_data.get("amenities", [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = set()

        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    places.update(state.places)

        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.update(city.places)

        if not states and not cities:
            places = storage.all(Place).values()

        if amenities:
            amenities = set(amenities)
            places = [place for place in places if \
                      amenities.issubset(place.amenities)]

    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)
