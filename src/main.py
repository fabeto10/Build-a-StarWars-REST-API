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
@app.route('/')
def sitemap():
    return generate_sitemap(app)

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
        lambda favorite_character: favorite_character.serialize(),
        characters
    ))
    favorites_planets = list(map(
        lambda favorite_planets: favorite_planets.serialize(),
        planets
    ))
    favorites = favorites_characters + favorites_planets

    return jsonify(favorites), 200

@app.route('/users/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_user_planet(planet_id):
    body = request.json
    favorite = FavoritePlanet(
            user_id = body["users_id"] if "users_id" in body else None, 
            planet_id = body["planet_id"] if "planet_id" in body else None
        )
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/users/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_user_character(people_id):
    body = request.json
    favorite = FavoriteCharacter(
        user_id= body["user_id"] if "user_id" in body else None,
        character_id= body["charcater_id"] if "charcater_id" in body else None
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    result = FavoriteCharacter.query.filter(FavoriteCharacter.character_id == people_id).delete()
    return jsonify(result), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    result = FavoritePlanet.query.filter(FavoritePlanet.planet_id == planet_id).delete()
    return jsonify(result), 200

@app.route('/llenarbd', methods=['POST'])
def llenarbd():
    r_body = request.json
    response = requests.get(f"https://www.swapi.tech/api/people?page=1&limit={r_body['limit']}")
    body = response.json()
    characters = body['results']
    new=0
    for character in characters:
        exist = Character.query.filter_by(name=character['name']).one_or_none()
        if exist: continue
        _response = requests.get(f"https://www.swapi.tech/api/people/{character['uid']}")
        _body = _response.json()
        properties = _body['result']['properties']
        _character = Character(
            name= properties["name"],
            hair_color= properties["hair_color"], 
            gender = properties["gender"],
            height = properties["height"]
        )
        new+=1
        db.session.add(_character)
    try:
        db.session.commit()
        return jsonify(f"added {new} characters"),200
    except Exception as error:
        db.session.rollback()
        return jsonify(f"{error.args}"), 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
