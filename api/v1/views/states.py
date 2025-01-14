#!/usr/bin/python3
"""
Defines the API routes for handling State objects
"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views
from flasgger import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from("../swaggerdocs/states/get_states.yml", methods=["GET"])
def get_states():
    """ Retrieves the list of all State objects """
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from("../swaggerdocs/states/get_state_id.yml", methods=["GET"])
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from("../swaggerdocs/states/delete.yml", methods=["DELETE"])
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from("../swaggerdocs/states/post.yml", methods=["POST"])
def create_state():
    """ Creates a State """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from("../swaggerdocs/states/put.yml", methods=["PUT"])
def update_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
