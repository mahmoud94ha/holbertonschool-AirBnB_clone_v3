#!/usr/bin/python3
"""
Contains the api app.py
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from os import environ
stype = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'])
def amenities_per_place(place_id=None):
    """amenities_per_place"""

    try:
        place = storage.get('Place', place_id)
    except AttributeError:
        place = None
    if place is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        if place is None:
            abort(404, 'Not found')
        amenities_all = storage.all('Amenity')
        if stype == 'db':
            place_amenities = place.amenities
        else:
            place_amen_ids = place.amenities
            place_amenities = []
            for amen in place_amen_ids:
                stype.append(storage.get('Amenity', amen))
        place_amenities = [
            obj.to_json() for obj in place_amenities
            ]
        return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_to_place(place_id=None, amenity_id=None):
    """amenity_to_place"""

    try:
        place = storage.get('Place', place_id)
    except AttributeError:
        place = None
    if place is None:
        abort(404, 'Not found')

    amenity_obj = storage.get('Amenity', amenity_id)
    if place is None:
        abort(404, 'Not found')
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if (amenity_obj not in place.amenities and
                amenity_obj.id not in place.amenities):
            abort(404, 'Not found')
        if stype == 'db':
            place.amenities.remove(amenity_obj)
        else:
            place.amenity_ids.pop(amenity_obj.id, None)
        place.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if (amenity_obj in place.amenities or
                amenity_obj.id in place.amenities):
            return jsonify(amenity_obj.to_json()), 200
        if stype == 'db':
            place.amenities.append(amenity_obj)
        else:
            place.amenities = amenity_obj
        return jsonify(amenity_obj.to_json()), 201
