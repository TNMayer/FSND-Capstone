#-*- coding: UTF-8 -*-

import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from errors import error_404, error_422, error_400, error_405, error_403, error_500, error_authError
from database.models import db_drop_and_create_all, setup_db, db, Movie, Actor, Casting
from auth.auth import AuthError, requires_auth, TOKEN_URL

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response
  
  # To initialize the database and populate it with dummy data for the first time (!!!), please uncomment line below
  # if test_config is None:
  #   db_drop_and_create_all()

  @app.route('/')
  def api_greeting():
    return jsonify({'message':'Hello World'})

  @app.route('/token')
  def get_token():
    return redirect(TOKEN_URL, code=302)

  @app.route('/auth')
  def return_token():
    return jsonify({
      'token': request.args.get('access_token')
    })

  # GET /actors and /movies
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    selection = Actor.query.order_by(Actor.id).all()
    
    if len(selection) == 0:
      return jsonify({
        'message': 'There are no actors in the database to display'
      })
    
    all_actors = []
    for actor in selection:
      all_actors.append(actor.format())

    return jsonify({
      'success': True,
      'actors': all_actors
    })
  
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:actors')
  def get_movies(jwt):
    selection = Movie.query.order_by(Movie.id).all()
    
    if len(selection) == 0:
      abort(404)
      # return jsonify({
      #   'error': 404,
      #   'message': 'There are no movies in the database to display'
      # })
    
    all_movies = []
    for movie in selection:
      all_movies.append(movie.format())
    
    return jsonify({
      'success': True,
      'movies': all_movies
    })

  @app.route('/castings', methods=['GET'])
  @requires_auth('get:castings')
  def get_castings(jwt):
    selection = Casting.query.order_by(Casting.movie_id, Casting.actor_id).all()

    if len(selection) == 0:
      abort(404)
      # return jsonify({
      #   'error': 404,
      #   'message': 'There are no castings in the database to display'
      # })
    
    all_castings = []
    for casting in selection:
      all_castings.append(casting.format())
    
    return jsonify({
      'success': True,
      'castings': all_castings
    })
  
  # DELETE /actors/ and /movies/
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(jwt, actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      castingSelection = Casting.query.filter(Casting.actor_id == actor_id).all()

      if actor is None:
          abort(404)

      for casting in castingSelection:
        casting.delete()
      
      actor.delete()

      return jsonify({
          'success': True,
          'message': 'Requested actor AND all related castings successfully removed!',
          'delete': actor_id
      }), 200
    except:
      abort(422)
  
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(jwt, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      castingSelection = Casting.query.filter(Casting.movie_id == movie_id).all()

      if movie is None:
        abort(404)

      print(movie.id)
      print(movie.title)

      movie.delete()

      for casting in castingSelection:
        casting.delete()

      return jsonify({
          'success': True,
          'message': 'Requested movie AND all related castings successfully removed!',
          'delete': movie_id
      }), 200
    except:
      abort(422)
  
  @app.route('/castings/<int:casting_id>', methods=['DELETE'])
  @requires_auth('delete:castings')
  def delete_castings(jwt, casting_id):
    try:
      castingSelection = Casting.query.filter(Casting.id == casting_id).all()

      if len(castingSelection) == 0:
        abort(404)

      for casting in castingSelection:
        casting.delete()

      return jsonify({
        'success': True,
        'delete': casting_id
      }), 200
    except:
      abort(422)
  
  # POST /actors and /movies

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(jwt):
    body = request.get_json()
    new_name = body['name']
    new_age = body['age']
    new_gender = body['gender']
    new_insertion_time = datetime.now()

    try:
      if ((new_name is None) or (new_age is None) or\
          (new_gender == '') or (new_insertion_time == '')):
        abort(404)
      
      actor = Actor(name=new_name, age=new_age, gender=new_gender, insertion_datetime=new_insertion_time)
      actor.insert()

    except:
        abort(422)

    return jsonify({
        'success': True, 
        'actor': actor.format()
    }), 200

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(jwt):
    body = request.get_json()
    new_title = body['title']
    new_release_date = body['release_date']
    new_insertion_time = datetime.now()

    try:
      if ((new_title is None) or (new_release_date is None) or\
          (new_insertion_time == '')):
        abort(404)
      
      movie = Movie(title=new_title, release_date=new_release_date, insertion_datetime=new_insertion_time)
      movie.insert()

    except:
        abort(422)

    return jsonify({
        'success': True, 
        'movie': movie.format()
    }), 200
  
  @app.route('/castings', methods=['POST'])
  @requires_auth('post:castings')
  def create_casting(jwt):
    body = request.get_json()
    new_movie_id = body['movie_id']
    new_actor_id = body['actor_id']
    new_insertion_time = datetime.now()

    try:
      if ((new_movie_id is None) or (new_actor_id is None) or\
          (new_insertion_time == '')):
        abort(404)
      
      casting = Casting(movie_id=new_movie_id, actor_id=new_actor_id, insertion_datetime=new_insertion_time)
      casting.insert()

    except:
        abort(422)

    return jsonify({
        'success': True, 
        'casting': casting.format()
    }), 200
  
  # PATCH /actors/ and /movies/

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(jwt, actor_id):
    # get all drinks with drink_id
    actor = Actor.query.filter(Actor.id == actor_id).first()

    # check if query returns drinks
    if not actor:
      abort(404)
    
    # get the posted body
    body = request.get_json()

    try:
      actor_name = body.get('name')
      actor_age = body.get('age')
      actor_gender = body.get('gender')
      
      if actor_name:
        actor.name = actor_name
        
      if actor_age:
        actor.age = actor_age
      
      if actor_gender:
        actor_gender = actor_gender
        
      actor.update()
    except:
      abort(422)
    
    return jsonify({
      'success': True,
      'actors': actor.format()
    }), 200
  
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(jwt, movie_id):
    # get all drinks with drink_id
    movie = Movie.query.filter(Movie.id == movie_id).first()

    # check if query returns drinks
    if not movie:
      abort(404)
    
    # get the posted body
    body = request.get_json()

    try:
      movie_title = body.get('title')
      movie_release_date = body.get('release_date')
      
      if movie_title:
        movie.title = movie_title
        
      if movie_release_date:
        movie.release_date = movie_release_date
        
      movie.update()
    except:
      abort(422)
    
    return jsonify({
      'success': True,
      'movies': movie.format()
    }), 200
  
  @app.route('/castings/<int:casting_id>', methods=['PATCH'])
  @requires_auth('patch:castings')
  def update_casting(jwt, casting_id):
    # get all drinks with drink_id
    casting = Casting.query.filter(Casting.id == casting_id).first()

    # check if query returns drinks
    if not casting:
      abort(404)
    
    # get the posted body
    body = request.get_json()

    try:
      casting_actor_id = body.get('actor_id')
      casting_movie_id = body.get('movie_id')
      
      if casting_actor_id:
        casting.actor_id = casting_actor_id
        
      if casting_movie_id:
        casting.movie_id = casting_movie_id
        
      casting.update()
    except:
      abort(422)
    
    return jsonify({
      'success': True,
      'castings': casting.format()
    }), 200
  
  error_404(app)
  error_422(app)
  error_400(app)
  error_405(app)
  error_403(app)
  error_500(app)
  error_authError(app, AuthError)
   
  return app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True, use_debugger=False, host='127.0.0.1', port=8080, use_reloader=True)