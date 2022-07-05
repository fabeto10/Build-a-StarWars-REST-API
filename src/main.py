"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
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

@app.route('/people/<int:character_id>', methods=["GET"])
def list_single_character(character_id):
    character = Character.query.filter_by(id=character_id).one_or_none()
    return jsonify(character.serialize())

@app.route('/planet', methods=['GET'])
def list_planets():
    planets = Planet.query.all()
    planets_dictionary = list(map(
        lambda planet: planet.serialize(),
        planets
    ))
    return jsonify(planets_dictionary)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
