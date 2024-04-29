#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """returns all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """returns review by id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """creates a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    review_data = request.get_json()
    if 'user_id' not in review_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, review_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in review_data:
        abort(400, 'Missing text')
    review_data['place_id'] = place_id
    review = Review(**review_data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """updates a review by id"""
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, 'Not a JSON')
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, value)
        review.save()
        return make_response(jsonify(review.to_dict()), 200)
    else:
        abort(404)
