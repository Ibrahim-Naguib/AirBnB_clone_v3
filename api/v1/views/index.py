#!/usr/bin/python3
"""module index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns json status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    stats_dict = {}
    for key, value in classes.items():
        stats_dict[key] = storage.count(value)
    return jsonify(stats_dict)
