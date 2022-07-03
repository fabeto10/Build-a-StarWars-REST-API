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
    favorite = db.relationship("favorite", back_populates="parent")

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("user", back_populates="children")
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    # user = db.relationship("favorite", back_populates="children")
    planet = db.Column(db.String(250), nullable=False)
    character = db.Column(db.String(250), nullable=False)

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    favorite_id = db.Column(db.Integer, ForeignKey("favorite.id"))
    favorite = db.relationship("favorite", back_populates="children")

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable= False)
    gender = db.Column(db.String(250), nullable=False)
    favorite_id = db.Column(db.Integer, ForeignKey("favorite.id"))
    favorite = db.relationship("favorite", back_populates="children")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }