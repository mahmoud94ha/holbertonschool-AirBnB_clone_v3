#!/usr/bin/python3
"""
Contains the api app.py
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flasgger import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/cities/get_cities.yml", methods=["GET"])
def get_cities_by_state(state_id):
    """get_cities_by_state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/cities/get_city_id.yml", methods=["GET"])
def get_city(city_id):
    """get_city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/cities/delete.yml", methods=["DELETE"])
def delete_city(city_id):
    """delete_city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/cities/post.yml", methods=["POST"])
def create_city(state_id):
    """create_city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    data['state_id'] = state_id
    city = City(**data)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/cities/put.yml", methods=["PUT"])
def update_city(city_id):
    """update_city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
