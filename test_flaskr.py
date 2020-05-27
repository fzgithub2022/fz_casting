import unittest
import json
import os

from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Movies, Actors


# Create Test Case
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

        # get auth tokens
        bearer = 'bearer '
        catoken = bearer + os.environ['CATOKEN']
        cdtoken = bearer + os.environ['CDTOKEN']
        eptoken = bearer + os.environ['EPTOKEN']

        # Creative Assistant Header
        self.ca_header = {'Authorization': catoken}

        # Creative Direcctor Header
        self.cd_header = {'Authorization': cdtoken}

        # Executive Producer Header
        self.ep_header = {'Authorization': eptoken}

        # Sample Actor
        self.new_actor = {
            'name': 'Keanu Reeves',
            'age': 54,
            'gender': 'Female'
        }

        # Sample Movie
        self.new_movie = {
            'name': 'The Matrix',
            'rdate': 'March 30, 1999'
        }

    def tearDown(self):
        pass

    # Executive Producers POST /movies should succeed
    def test_insert_movie(self):
        res = self.client().post('/movies',
                                 headers=self.ep_header, json=self.new_movie)
        data = json.loads(res.data)
        if res.status_code == 201:
            self.assertEqual(res.status_code, 201)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    # Creative Director POST /movies should succeed
    def test_insert_actor(self):
        res = self.client().post('/actors',
                                 headers=self.cd_header, json=self.new_actor)
        data = json.loads(res.data)
        if res.status_code == 201:
            self.assertEqual(res.status_code, 201)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    # Createive Assistant GET /movies should succeed
    def test_movies(self):
        res = self.client().get('/movies', headers=self.ca_header)
        data = json.loads(res.data)
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    # Create Assistant GET /actors should succeed
    def test_actors(self):
        res = self.client().get('/actors', headers=self.ca_header)
        data = json.loads(res.data)
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    # Creative Assistant /movies should fail with 403
    def test_insert_movie_ca(self):
        res = self.client().post('/movies',
                                 headers=self.ca_header, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Creative Assistant /actors should fail with 403
    def test_insert_actor_ca(self):
        res = self.client().post('/actors',
                                 headers=self.ca_header, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Executive Producer PATCH /movies/<int:m_id> should succeed
    def test_patching_movie(self):
        res = self.client().patch('/movies/1',
                                  headers=self.ep_header,
                                  json={'rdate': 'March 31, 1999'})
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(movie.format()['rdate'], 'March 31, 1999')
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    # Creative Director PATCH /actors/<int:a_id> should succeed
    def test_patching_actor(self):
        res = self.client().patch('/actors/1',
                                  headers=self.cd_header,
                                  json={'age': 55, 'gender': 'Male'})
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == 1).one_or_none()
        if res.status_code == 200:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(actor.format()['age'], 55)
        else:
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)

    # Creative Assistant /movies/<int:m_id>/ should fail with 403
    def test_patching_movie(self):
        res = self.client().patch('/movies/1',
                                  headers=self.ca_header,
                                  json={'rdate': 'March 31, 1999'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Creative Assistant /actors/<int:m_id>/ should fail with 403
    def test_patching_actor(self):
        res = self.client().patch('/actors/1',
                                  headers=self.ca_header,
                                  json={'age': 55, 'gender': 'Male'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Executive Producer DELETE /movies/<int:m_id>/ should succeed
    def delete_movie_ep(self):
        res = self.client().delete('/movies/1',
                                   headers=self.ep_header)
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

    # Creative Director DELETE /actors/<int:a_id>/ should succeed
    def delete_actor_cd(self):
        res = self.client().delete('/actors/1', headers=self.cd_header)
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

    # Creative Assistant /movies/<int:m_id>/ should fail with 403
    def delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.ca_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Creative Assistant /actors/<int:m_id>/ should fail with 403
    def delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.ca_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


if __name__ == '__main__':
    unittest.main()
