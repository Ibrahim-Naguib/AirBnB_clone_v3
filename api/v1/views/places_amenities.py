#!/usr/bin/python3
"""handles all default RESTFul API actions"""
import os
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """returns all amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_object = place.amenities
    else:
        amenity_object = place.amenity_ids
    for amenity in amenity_object:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes amenity by id"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """creates a new amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
