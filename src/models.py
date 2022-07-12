from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planet = db.relationship("FavoritePlanet", back_populates="user")
    favorite_character = db.relationship("FavoriteCharacter", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email":self.email,
            "password":self.password,
            "is_active":self.is_active
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", back_populates=__tablename__)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet", back_populates="favorite_planet")
    
    def __init__(self, user_id, planet_id):
        self.user_id = user_id
        self.planet_id = planet_id
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", back_populates="favorite_character")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    character = db.relationship("Character", back_populates="favorite_character")
    
    def __init__(self, user_id, character_id):
        self.user_id = user_id
        self.character_id = character_id
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    favorite_planet = db.relationship("FavoritePlanet", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "population":self.population,
            "terrain":self.terrain
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable= False)
    gender = db.Column(db.String(250), nullable=False)
    favorite_character = db.relationship("FavoriteCharacter", back_populates="character")

    # def __repr__(self):
    #     return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height":self.height,
            "hair_color":self.hair_color
        }