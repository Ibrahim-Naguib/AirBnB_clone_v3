#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """returns all amenities"""
    amenities = []
    for key, value in storage.all(Amenity).items():
        amenities.append(value.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """returns amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """creates a new amenity"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        return abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """updates a amenity by id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
    else:
        return abort(404)
