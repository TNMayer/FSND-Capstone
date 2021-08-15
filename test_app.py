import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import create_app
from database.models import setup_db, db_drop_and_create_all, Actor, Movie, Casting

class FsndCapstoneTesting(unittest.TestCase):
    '''
    Testcases for capstone project
    '''

    def setUp(self):
        '''
        initialize test database
        fill test database with testdata
        set needed variables
        '''
        self.TOKEN_ASSISTANT = os.environ['TOKEN_ASSISTANT']
        self.TOKEN_DIRECTOR = os.environ['TOKEN_DIRECTOR']
        self.TOKEN_PRODUCER = os.environ['TOKEN_PRODUCER']
        self.app = create_app(test_config='test')
        self.client = self.app.test_client
        setup_db(self.app, setting="test")

        self.CREATE_ACTOR_PASS = {
            "name": "Moritz Stefaner",
            "age": 48,
            "gender": "male"
        }
        self.CREATE_ACTOR_FAIL = {
            "name": "Moritz Stefaner"
        }
        self.UPDATE_ACTOR_PASS = {
            "name": "Analena Baerbock"
        }
        self.CREATE_MOVIE_PASS = {
            "title": "Suicidal Tendencies 555",
            "release_date": "2025-07-31"
        }
        self.CREATE_MOVIE_FAIL = {
            "title": "Suicidal Tendencies"
        }
        self.UPDATE_MOVIE_PASS = {
            "title": "Friedhof der Kuscheltiere"
        }
        self.CREATE_CASTING_PASS = {
            "movie_id": 4,
            "actor_id": 1
        }
        self.UPDATE_CASTING_PASS = {
            "movie_id": 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        db_drop_and_create_all()
        pass

    '''
    Test for endpoint /
    '''

    def test_api_init(self):
        """Pass: GET for endpoint /"""
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Hello World')
    
    '''
    Tests for endpoint /actors
    '''

    def test_get_actors_401(self):
        """Fail: GET on /actors without token"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_actors_assistant(self):
        """Pass: GET with role Assistant on /actors"""
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_ASSISTANT)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('actors', data)
        self.assertTrue(len(data["actors"]))
    
    def test_post_actors_assistant_403(self):
        """Fail: 403 Unauthorized"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_ASSISTANT)
        }, json=self.CREATE_ACTOR_PASS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], "Permission not found.")
    
    def test_post_actors_director(self):
        """Pass"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_DIRECTOR)
        }, json=self.CREATE_ACTOR_PASS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['name'], "Moritz Stefaner")
    
    def test_post_actors_director_500(self):
        """Fail: 500 Internal server error"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_DIRECTOR)
        }, json=self.CREATE_ACTOR_FAIL)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['message'], 'Internal Server Error')
    
    def test_post_actors_producer(self):
        """Pass"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        }, json=self.CREATE_ACTOR_PASS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['name'], "Moritz Stefaner")
    
    def test_patch_actors_producer(self):
        """Pass"""
        res = self.client().patch('/actors/4', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        }, json=self.UPDATE_ACTOR_PASS)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actors']['name'], 'Analena Baerbock')
    
    def test_delete_actors_producer(self):
        """Pass"""
        res = self.client().delete('/actors/3', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)

    '''
    Tests for endpoint /movies
    '''

    def test_get_movies_401(self):
        """Fail: GET on /movies without token"""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_movies_assistant(self):
        """Pass: GET with role Assistant on /movies"""
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_ASSISTANT)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('movies', data)
        self.assertTrue(len(data["movies"]))
    
    def test_post_movies_assistant_403(self):
        """Fail: 403 Unauthorized"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_ASSISTANT)
        }, json=self.CREATE_MOVIE_PASS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], "Permission not found.")
    
    def test_post_movies_director_403(self):
        """Fail: 403"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_DIRECTOR)
        }, json=self.CREATE_MOVIE_PASS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], "Permission not found.")
    
    def test_post_movies_producer_500(self):
        """Fail: 500 Internal server error"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        }, json=self.CREATE_MOVIE_FAIL)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['message'], 'Internal Server Error')
    
    def test_post_movies_producer(self):
        """Pass"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        }, json=self.CREATE_MOVIE_PASS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], self.CREATE_MOVIE_PASS['title'])
    
    def test_patch_movies_producer(self):
        """Pass"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        }, json=self.UPDATE_MOVIE_PASS)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movies']['title'], self.UPDATE_MOVIE_PASS['title'])
    
    def test_delete_actors_producer(self):
        """Pass"""
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
    
    '''
    Tests for endpoint /castings
    '''

    def test_get_castings_401(self):
        """Fail: GET on /actors without token"""
        res = self.client().get('/castings')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_castings_assistant(self):
        """Pass: GET with role Assistant on /castings"""
        res = self.client().get('/castings', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('castings', data)
        self.assertTrue(len(data["castings"]))
    
    def test_post_castings_assistant_403(self):
        """Fail: 403 Unauthorized"""
        res = self.client().post('/castings', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_ASSISTANT)
        }, json=self.CREATE_CASTING_PASS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], "Permission not found.")
    
    def test_post_castings_producer(self):
        """Pass"""
        res = self.client().post('/castings', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        }, json=self.CREATE_CASTING_PASS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
    
    def test_delete_castings_producer(self):
        """Pass"""
        res = self.client().delete('/castings/3', headers={
            'Authorization': "Bearer {}".format(self.TOKEN_PRODUCER)
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()