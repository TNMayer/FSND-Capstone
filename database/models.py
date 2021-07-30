import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

# PSQL Statements
# login as superuser in psql: e.g. psql -U postgres
# create database fsnd_capstone;
# create user fsnd with encrypted password 'fsnd';
# grant all privileges on database fsnd_capstone to fsnd;

# database_path = "./database/casting_agency.sqlite"
# database_path = "sqlite:///{}".format(database_path)

database_name = "fsnd_capstone"
database_path = "postgresql://{}:{}@{}/{}".format('fsnd', 'fsnd', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
    db_drop_and_create_all()
    drops the database tables and starts fresh
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    movie = Movie(
        title='The Shawshank Redemption',
        release_date = '1994-01-01',
        insertion_datetime = dt_string
    )

    movie.insert()

    actor = Actor(
        name = 'Bruce Willis',
        age = 66,
        gender = 'male',
        insertion_datetime = dt_string
    )

    actor.insert()

    actor2 = Actor(
        name = 'Drew Berrymore',
        age = 46,
        gender = 'female',
        insertion_datetime = dt_string
    )

    actor2.insert()

class Movie(db.Model):
    __tablename__ = 'Movies'

    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(255), unique=True)
    release_date = Column(String(20), nullable=False)
    insertion_datetime = Column(String(255), nullable=False)

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
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'insertion_datetime': self.insertion_datetime
        }

class Actor(db.Model):
    __tablename__ = 'Actors'

    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(255))
    age = Column(Integer())
    gender = Column(String(100))
    insertion_datetime = Column(String(255))

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