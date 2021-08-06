#-*- coding: UTF-8 -*-

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from datetime import datetime

# PSQL Statements
# login as superuser in psql: e.g. psql -U postgres
# create database fsnd_capstone;
# create user fsnd with encrypted password 'fsnd';
# grant all privileges on database fsnd_capstone to fsnd;

# database_path = "./database/casting_agency.sqlite"
# database_path = "sqlite:///{}".format(database_path)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, setting="default"):
    if setting == "default":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URI']
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_TEST_URI']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    # migrate = Migrate(app, db)
    db.init_app(app)

    # if setting != 'default':
    #     db_drop_and_create_all()

'''
    db_drop_and_create_all()
    drops the database tables and starts fresh
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    moviecollection = [
        {
            "title": 'The Shawshank Redemption',
            "release_date": '2022-07-31'
        },
        {
            "title": 'Der Pate',
            "release_date": '2022-05-25'
        },
        {
            "title": 'The Dark Knight',
            "release_date": '2022-03-18'
        },
        {
            "title": 'Die zwölf Geschworenen',
            "release_date": '2022-02-01'
        }
    ]

    actorcollection = [
        {
            "name": 'Johnny Depp',
            "age": 58,
            "gender": "male"
        },
        {
            "name": 'Russel Crowe',
            "age": 57,
            "gender": "male"
        },
        {
            "name": 'Brad Pitt',
            "age": 58,
            "gender": "male"
        },
        {
            "name": 'Bruce Willis',
            "age": 66,
            "gender": "female"
        },
        {
            "name": 'Cate Blanchett',
            "age": 52,
            "gender": "female"
        },
        {
            "name": 'Jodie Foster',
            "age": 59,
            "gender": "female"
        },
        {
            "name": 'Nicole Kidman',
            "age": 54,
            "gender": "female"
        },
    ]

    castingcollection = {
        1: [1, 4, 6],
        2: [2, 3, 5],
        3: [1, 2]
    }

    for movie in moviecollection:
        insertMovie = Movie(
            title=movie["title"],
            release_date = movie["release_date"],
            insertion_datetime = datetime.now()
        )
        insertMovie.insert()

    for actor in actorcollection:
        insertActor = Actor(
            name = actor["name"],
            age = actor["age"],
            gender = actor["gender"],
            insertion_datetime = datetime.now()
        )
        insertActor.insert()
    
    movieIds = list(castingcollection.keys())
    for movieId in movieIds:
        for actorId in castingcollection[movieId]:
            insertCasting = Casting(
                movie_id = movieId,
                actor_id = actorId,
                insertion_datetime = datetime.now()
            )
            insertCasting.insert()

class Movie(db.Model):
    __tablename__ = 'movies'

    # Autoincrementing, unique primary key
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    release_date = db.Column(db.String(20), nullable=False)
    insertion_datetime = db.Column(db.DateTime(), nullable=False)
    castings = db.relationship('Casting', backref="movies", lazy=True)

    def __init__(self, title, release_date, insertion_datetime):
        self.title = title
        self.release_date = release_date
        self.insertion_datetime = insertion_datetime

    def __repr__(self):
        return "<Movie {} {} {} {} />".format(self.id, self.title, self.release_date, self.insertion_datetime)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        # db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'insertion_datetime': self.insertion_datetime
        }

class Actor(db.Model):
    __tablename__ = 'actors'

    # Autoincrementing, unique primary key
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer())
    gender = db.Column(db.String(100))
    insertion_datetime = db.Column(db.DateTime(), nullable=False)
    castings = db.relationship('Casting', backref="actors", lazy=True)

    def __init__(self, name, age, gender, insertion_datetime):
        self.name = name
        self.age = age
        self.gender = gender
        self.insertion_datetime = insertion_datetime

    def __repr__(self):
        return "<Movie {} {} {} {} />".format(self.id, self.name, self.age, self.gender, self.insertion_datetime)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'insertion_datetime': self.insertion_datetime
        }

class Casting(db.Model):
    __tablename__ = 'castings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
    insertion_datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Show movie_id={self.artist_id}, actor_id={self.venue_id}, insertion_datetime={self.insertion_datetime}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        movie = Movie.query.filter(Movie.id == self.movie_id).first()
        movie_title = movie.title

        actor = Actor.query.filter(Actor.id == self.actor_id).first()
        actor_name = actor.name

        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'movie_title': movie_title,
            'actor_id': self.actor_id,
            'actor_name': actor_name,
            'insertion_datetime': self.insertion_datetime
        }