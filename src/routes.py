from flask import Flask, request, jsonify, Blueprint
from models import db, User, Planet, People, Favorite
from utils import generate_sitemap, APIException

api = Blueprint("api", __name__)

CURRENT_USER_ID = 1


@api.route("/hello", methods=["GET"])
def handle_hello():
    return jsonify({"message": "Hello! I'm a StarWars API"}), 200


# -----------------------
# PEOPLE
# -----------------------

@api.route("/people", methods=["GET"])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200


@api.route("/people/<int:people_id>", methods=["GET"])
def get_single_person(people_id):
    person = People.query.get(people_id)

    if person is None:
        return jsonify({"error": "Person not found"}), 404

    return jsonify(person.serialize()), 200


# -----------------------
# PLANETS
# -----------------------

@api.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    return jsonify(planet.serialize()), 200


# -----------------------
# USERS
# -----------------------

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@api.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user = User.query.get(CURRENT_USER_ID)

    if user is None:
        return jsonify({"error": "Current user not found"}), 404

    favorites = Favorite.query.filter_by(user_id=CURRENT_USER_ID).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200


# -----------------------
# FAVORITE PLANET
# -----------------------

@api.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user = User.query.get(CURRENT_USER_ID)
    planet = Planet.query.get(planet_id)

    if user is None:
        return jsonify({"error": "Current user not found"}), 404

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    existing_favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    ).first()

    if existing_favorite:
        return jsonify({"error": "Planet already in favorites"}), 400

    favorite = Favorite(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "message": "Planet added to favorites",
        "favorite": favorite.serialize()
    }), 201


@api.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    ).first()

    if favorite is None:
        return jsonify({"error": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Planet removed from favorites"}), 200


# -----------------------
# FAVORITE PEOPLE
# -----------------------

@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    user = User.query.get(CURRENT_USER_ID)
    person = People.query.get(people_id)

    if user is None:
        return jsonify({"error": "Current user not found"}), 404

    if person is None:
        return jsonify({"error": "Person not found"}), 404

    existing_favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    ).first()

    if existing_favorite:
        return jsonify({"error": "Person already in favorites"}), 400

    favorite = Favorite(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "message": "Person added to favorites",
        "favorite": favorite.serialize()
    }), 201


@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    ).first()

    if favorite is None:
        return jsonify({"error": "Favorite person not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Person removed from favorites"}), 200