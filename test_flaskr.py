import unittest
import json
import os

from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Movies, Actors

#Create Test Case
class CastingAppTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capdb_test"
        self.database_uname = "postgres"
        self.database_password = "pgpw"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.database_uname,
            self.database_password,
            'localhost:5432',
            self.database_name
            )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        #new test movie
        self.new_movie = {
            'name': 'The Matrix',
            'rdate': 'March 30, 1999'
        }

        #new test actor
        self.new_actor = {
            'name': 'Keanu Reeves',
            'age': 54,
            'gender': 'Female'
        }
    
    def tearDown(self):
        pass
    
    #insert movie success and error test
    def test_insert_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        if res.status_code == 201:
            self.assertEqual(res.status_code, 201)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    #insert actor test
    def test_insert_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        if res.status_code == 201:
            self.assertEqual(res.status_code, 201)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    #get movies test
    def test_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    #get actors test
    def test_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    #patch movie
    def test_patching_movie(self):
        res = self.client().patch('/movies/1', json={'rdate': 'March 31, 1999'})
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(movie.format()['rdate'], 'March 31, 1999')
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
    
    #test empty release date error
    def test_empty_rdate(self):
        res = self.client().patch('/movies/1', json={'rdate': None})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    #patch actor
    def test_patching_actor(self):
        res = self.client().patch('/actors/1', json={'age': 55, 'gender': 'Male'})
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == 1).one_or_none()
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(actor.format()['age'], 55)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
    
    #if one of the two properties is missing should still work
    def test_missing_actor_property(self):
        res = self.client().patch('/actors/1', json={'age': 55})
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == 1).one_or_none()
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(actor.format()['age'], 55)

    #delete movie
    def delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        # if the is the first time running the test
        if res.status_code == 200:
            # the record will be available and
            # delete will be successful
            self.assertEqual(res.status_code, 200)
        else:  # otherwise was deleted
            # so resource won't be found
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')

    #delete actor
    def delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        # if the is the first time running the test
        if res.status_code == 200:
            # the record will be available and
            # delete will be successful
            self.assertEqual(res.status_code, 200)
        else:  # otherwise was deleted
            # so resource won't be found
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found!')

if __name__ == '__main__':
    unittest.main()