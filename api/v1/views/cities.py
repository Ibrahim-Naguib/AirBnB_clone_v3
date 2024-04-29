#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """returns all cities"""
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """returns city by id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes city by id"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """creates a new city"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    city_data = request.get_json()
    if 'name' not in city_data:
        return abort(400, 'Missing name')
    city_data['state_id'] = state_id
    city = City(**city_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """updates a city by id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at', 'state_id']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        return abort(404)
