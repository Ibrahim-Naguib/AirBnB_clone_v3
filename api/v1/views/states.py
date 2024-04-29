#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """returns all states"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """returns state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """creates a new state"""
    kwargs = request.get_json(silent=True)
    if not kwargs:
        abort(400, description='Not a JSON')
    elif 'name' not in kwargs.keys():
        abort(400, description='Missing name')
    state = State(**kwargs)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """updates a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    kwargs = request.get_json(silent=True)
    if not kwargs:
        abort(400, description='Not a JSON')
    for key, value in kwargs.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
