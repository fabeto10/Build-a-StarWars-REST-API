"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

favorite_list = []

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/users/people', methods=["GET"])
def list_people():
    people = Character.query.all()
    people_dictionary = list(map(
        lambda character: character.serialize(),
        people
    ))
    return jsonify(people_dictionary)

@app.route('/users/people/<int:people_id>', methods=["GET"])
def list_single_people(people_id):
    character = Character.query.filter_by(id=people_id).one_or_none()
    return jsonify(character.serialize())

@app.route('/users/planet', methods=['GET'])
def list_planets():
    planets = Planet.query.all()
    planets_dictionary = list(map(
        lambda planet: planet.serialize(),
        planets
    ))
    return jsonify(planets_dictionary)

@app.route('/users/planet/<int:planet_id>', methods=["GET"])
def list_single_planet(planet_id):
    planet = Planet.query.filter_by(planet_id).one_or_none()
    return jsonify(planet.serialize())

@app.route('/users', methods=['GET'])
def list_user_blog(user_id):
    users = User.query.all()
    user_dictionary = list((map(lambda user: user.serialize(), users)))
    return jsonify(user_dictionary)

@app.route('/users/favorites/<int:planet_id>', methods=['GET'])
def list_favorite_user_planet(planet_id):
    user_favorite_list_planet = User.query.filter_by(planet_id).one_or_none()
    return serialize(user_favorite_list_planet), 200

@app.route('/users/favorites/<int:people_id>', methods=['GET'])
def list_favorite_user_people(people_id):
    user_favorite_list_people = User.query.filter_by(people_id).one_or_none()
    return serialize(user_favorite_list_people), 200

@app.route('/users/favorites/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    global favorite_list
    favorite_list.append(planet_id)
    return jsonify(favorite_list), 200

@app.route('/users/favorites/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    global favorite_list
    favorite_list.append(people_id)
    return jsonify(favorite_list), 200

@app.route('/users/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    aux = []
    global favorite_list
    for i in range(len(favorite_list)):
        if people_id != i:
            aux.append(favorite_list[i])
    favorite_list = aux
    return jsonify(favorite_list), 200

@app.route('/users/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    aux = []
    global favorite_list
    for i in range(len(favorite_list)):
        if planet_id != i:
            aux.append(favorite_list[i])
    favorite_list = aux
    return jsonify(favorite_list), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
