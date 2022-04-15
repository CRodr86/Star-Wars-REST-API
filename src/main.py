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
from models import db, User, Character, Planet, Favorites

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

# User endpoints
@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user_x = User.query.get(user_id)
    if user_x is None:
        return 'User not found', 404
    else:
        return jsonify(user_x.serialize()), 200

@app.route('/user', methods=['POST'])
def create_users():
    request_body = request.get_json()
    new_user = User(name= request_body["name"], email= request_body["email"], password= request_body["password"], favorite_planet= request_body["favorite_planet"], favorite_character= request_body["favorite_character"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(request_body), 201

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_x = User.query.get(user_id)
    if user_x is None:
        return 'User not found', 404
    else:
        db.session.delete(user_x)
        db.session.commit()
        return jsonify("User deleted"), 200

# Character endpoints
@app.route('/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(all_characters), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    character_x = Character.query.get(character_id)
    if character_x is None:
        return 'Character not found', 404
    else:
        return jsonify(character_x.serialize()), 200

@app.route('/character', methods=['POST'])
def create_character():
    request_body = request.get_json()
    new_character = Character(name= request_body["name"])
    db.session.add(new_character)
    db.session.commit()
    return jsonify(request_body), 201

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character_x = Character.query.get(character_id)
    if character_x is None:
        return 'Character not found', 404
    else:
        db.session.delete(character_x)
        db.session.commit()
        return jsonify("Character deleted"), 200

#Planet endpoints
@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

@app.route('/planet/<int:planets_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet_x = Planet.query.get(planet_id)
    if planet_x is None:
        return 'Planet not found', 404
    else:
        return jsonify(planet_x.serialize()), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet(name= request_body["name"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(request_body), 201

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet_x = Planet.query.get(planet_id)
    if planet_x is None:
        return 'Planet not found', 404
    else:
        db.session.delete(planet_x)
        db.session.commit()
        return jsonify("Planet deleted"), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
