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
    favorites = relationship("Favorite", back_populates="user")

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    planet = db.Column(db.String(250), nullable=False)
    character = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    planet_id = Column(Integer, ForeignKey("planet.id"))
    planet =relationship("Planet", back_populates="favorites")
    character_id = Column(Integer, ForeignKey("character.id"))
    character = relationship("Character", back_populates="favorites")

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    favorites = relationship("Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # "": self.gender
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable= False)
    gender = db.Column(db.String(250), nullable=False)
    favorites = relationship("Favorite", back_populates="character")

    # def __repr__(self):
    #     return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender
            # do not serialize the password, its a security breach
        }