from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import json
from flask_migrate import Migrate
from models import setup_db, Movies, Actors, db
from auth import AuthError, requires_auth

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__)

    #connect to databse and models
    setup_db(app)

    #enable flask_migrate
    migrate = Migrate(app, db)

    #enable cross-origins
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    #set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE')
        return response

    #Insert Movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        body = request.get_json()
        name = body.get('name')
        rdate = body.get('rdate')
        try:
            movie = Movies(
                name = name,
                rdate = rdate
            )
            Movies.insert(movie)
        except BaseException:
            abort(404)
        return jsonify({
            'status': 'Successfully added a movie',
            'success': True
        }), 201

    #Insert Actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        try:
            actor = Actors(
                name = name,
                age = age,
                gender = gender
            )
            Actors.insert(actor)
        except BaseException:
            abort(404)
        return jsonify({
            'status': 'Successfully added a actor',
            'success': True
        }), 201

    #Get Movies Decorator
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.all()
            formatted_movies = [movie.format() for movie in movies]
        except BaseException:
            abort(404)
        return jsonify({
            'movies': formatted_movies,
            'success': True
        }), 200

    #Get Actors Decorator
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload): #add payload when ready
        try:
            actors = Actors.query.all()
            formatted_actors = [actor.format() for actor in actors]
        except BaseException:
            abort(404)
        return jsonify({
            'Actors': formatted_actors,
            'success': True
        }), 200

    #Patch movie
    @app.route('/movies/<int:m_id>', methods=['PATCH'])
    @requires_auth('modify:movies')
    def patch_movie(m_id, payload):
        body = request.get_json()
        try:
            movie = Movies.query.filter(Movies.id == m_id).one_or_none()
            if movie is None:
                abort(404)
        except BaseException:
            abort(404)
        rdate = body.get('rdate')
        if rdate is None:
            abort(400)
        movie.rdate = rdate
        Movies.update(movie)
        return jsonify ({
            "status": "Movie updated",
            "success": True
        }), 200

    #Patch Actor
    @app.route('/actors/<int:a_id>', methods=['PATCH'])
    @requires_auth('modify:actors')
    def patch_actor(a_id, payload):
        body = request.get_json()
        try:
            actor = Actors.query.filter(Actors.id == a_id).one_or_none()
            if actor is None:
                abort(404)
        except BaseException:
                abort(404)
        age = body.get('age')
        gender = body.get('gender')
        if age is None and gender is None:
            abort(400)
        actor.age = age
        actor.gender = gender
        Actors.update(actor)
        return jsonify({
            "status": "Actor updated successfully",
            "success": True
        }), 200

    #Delete Movie
    @app.route('/movies/<int:m_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def del_movie(payload, m_id):
        try:
            movie = Movies.query.filter(Movies.id == m_id).one_or_none()
            movie.delete()
        except BaseException:
            abort(404)
        return jsonify({
            'status': 'Deleted Successful'
        }), 200

    #Delete Actor
    @app.route('/actors/<int:m_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def del_actor(payload, a_id):
        try:
            actor = Actors.query.filter(Actors.id == a_id).one_or_none()
            actor.delete()
        except BaseException:
            abort(404)
        return jsonify({
            'status': 'Deleted Successful'
        }), 200

    #error handlers
    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({
            'message': 'bad request! shame on you',
            'success': False
        }), 400
    
    @app.errorhandler(AuthError)
    def handle_401(AuthError):
        status_code = AuthError.status_code
        error = AuthError.error
        if status_code == 400:
            return jsonify({
                'message': error,
                'success': False
            }), 400
        if status_code == 401:
            return jsonify({
                'message': error,
                'success': False
            }), 401
        if status_code == 403:
            return jsonify({
                'message': 'Hey, you\'re not allowed to that',
                'success': False
            }), 403

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            'message': 'resource not found!',
            'success': False
        }), 404

    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({
            'message': 'method NOT allowed!',
            'success': False
        }), 405

    return app