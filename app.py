import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from errors import error_404, error_422, error_400, error_405, error_500, error_authError
from database.models import db_drop_and_create_all, setup_db, db, Movie, Actor

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
  db_drop_and_create_all()

  @app.route('/')
  def api_greeting():
      return jsonify({'message':'Hello, World!'})

  @app.route('/actors', methods=['GET'])
  def get_actors():
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

  return app

APP = create_app()

if __name__ == '__main__':
  APP.run(debug=True, use_debugger=False, host='127.0.0.1', port=8080, use_reloader=True)