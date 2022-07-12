"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import requests
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoritePlanet, FavoriteCharacter
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/people', methods=["GET"])
def list_people():
    people = Character.query.all()
    people_dictionary = list(map(
        lambda character: character.serialize(),
        people
    ))
    return jsonify(people_dictionary)

@app.route('/people/<int:people_id>', methods=["GET"])
def list_single_people(people_id):
    character = Character.query.filter_by(id=people_id).one_or_none()
    return jsonify(character.serialize())

@app.route('/planets', methods=['GET'])
def list_planets():
    planets = Planet.query.all()
    planets_dictionary = list(map(
        lambda planet: planet.serialize(),
        planets
    ))
    return jsonify(planets_dictionary)

@app.route('/planets/<int:planet_id>', methods=["GET"])
def list_single_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).one_or_none()
    return jsonify(planet.serialize())

@app.route('/users', methods=['GET'])
def list_user_blog():
    users = User.query.all()
    user_dictionary = list(map(lambda user: user.serialize(), users))
    return jsonify(user_dictionary)

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    characters = FavoriteCharacter.query.all()
    planets = FavoritePlanet.query.all()
    favorites_characters = list(map(
        lambda favorite_character: characters.serialize(),
        characters
    ))
    favorites_planets = list(map(
        lambda favorite_planets: planets.serialize(),
        planets
    ))
    favorites = favorites_character + favorites_planets

    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_user_planet(planet_id):
    planet_id=data.planet_id
    user_id=data.user_id
    newFavoritePlanet = FavoritePlanet(user_id=data["user_id"], planet_id=data["planet_id"])
    return newFavoritePlanet, 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_user_character(people_id):
    people_id=data.people_id
    user_id=data.user_id
    newFavoritePeople = FavoriteCharacter(user_id=data["user_id"], character_id=data['people_id'])
    return newFavoritePeople, 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    result = FavoriteCharacter.query.filter(FavoriteCharacter.character_id == people_id).delete()
    return jsonify(result), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    result = FavoritePlanet.query.filter(FavoritePlanet.planet_id == planet_id).delete()
    return jsonify(result), 200


# def delete_favorite_people(people_id):
#     aux = []
#     global favorite_people
#     for i in range(len(favorite_people)):
#         if people_id != i:
#             aux.append(favorite_people[i])
#     favorite_people = aux
#     return jsonify(favorite_people), 200


# @app.route('/llenarbd', methods='POST')
# def llenarbd():
#     r_body = request.json
#     response = request.get(f"https://www.swapi.tech/api/people?page=1&limit={r_body['limit']}")
#     body =request.json()
#     characters = body["results"]
#     new = 0
#     for character in characters:
#         exist = Character.query.filter_by(name=character['name']).one_or_none() 
#         if exist: continue
#         _response = request.get(f"https://www.swapi.tech/api/people/{character['uid']}")
#         _body = _response.json()
#         properties = _body['result']['properties']
#         _character = Character( 
#             name=properties['name'], 
#             hair_color=properties['hair_color'], 
#             gender=properties['gender'], 
#             height=properties['height']
#                     )
#         new += 1
#         db.session.add(_character)
#     try:
#         db.session.commit()
#         return jsonify(f"added {new} characters"),200
#     except Exception as error:
#         db.session.rollback()
#     return jsonify(f"{error.args}"), 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
