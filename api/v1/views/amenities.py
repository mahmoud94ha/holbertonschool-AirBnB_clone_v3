#!/usr/bin/python3
"""
Contains the api app.py
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from flasgger import swag_from
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/amenities/get_amenities.yml", methods=["GET"])
@swag_from("../swaggerdocs/amenities/post.yml", methods=["POST"])
def get_amenities():
    """get_amenities"""
    amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/amenities/get_amenity_id.yml", methods=["GET"])
def get_amenity(amenity_id):
    """get_amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/amenities/delete.yml", methods=["DELETE"])
def delete_amenity(amenity_id):
    """delete_amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/amenities/post.yml", methods=["POST"])
def create_amenity():
    """create_amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenity = Amenity(**request.get_json())
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/amenities/put.yml", methods=["PUT"])
def update_amenity(amenity_id):
    """update_amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())
