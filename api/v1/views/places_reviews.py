#!/usr/bin/python3
"""
Contains the api app.py
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flasgger import swag_from


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
@swag_from("../swaggerdocs/places_reviews/get_reviews.yml", methods=["GET"])
def retrieves_all_reviews(place_id):
    """retrieves_all_reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from("../swaggerdocs/places_reviews/get_review_id.yml", methods=["GET"])
def get_reviews(review_id):
    """get_reviews"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from("../swaggerdocs/places_reviews/delete.yml", methods=["DELETE"])
def delete_review(review_id):
    """delete_review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
@swag_from("../swaggerdocs/places_reviews/post.yml", methods=["POST"])
def create_review(place_id):
    """create_review"""
    review_data = request.get_json()
    if not review_data:
        abort(400, 'Not a JSON')

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if "user_id" not in review_data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, review_data.get("user_id"))
    if not user:
        abort(404)
    if "text" not in review_data.keys():
        abort(400, "Missing text")

    review_data["place_id"] = place_id
    new_review = Review(**review_data)
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from("../swaggerdocs/places_reviews/put.yml", methods=["PUT"])
def update_review(review_id):
    """update_review"""
    review_data = request.get_json()
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    elif not review_data:
        abort(400, "Not a JSON")

    for key, value in review_data.items():
        list = ["id", "user_id", "place_id",
                "created_at", "updated_at"]
        if key not in list:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
