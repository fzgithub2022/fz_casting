from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import json
from models import setup_db, Movies, Actors

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__)
    setup_db(app) #connect to databse and models

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
    
    #Get Movies Decorator
    @app.route('/movies', methods=['GET'])
    def get_movies():
        query_movies = Movies.query.all()
        movies = {}
        for movie in query_movies:
            movies[movie.id] = movie.name
        return jsonify({
            'movies': movies
        }), 200
    
    #Get Actors Decorator
    @app.route('/actors', methods=['GET'])
    def get_actors():
        query_actors = Actors.query.all()
        actors = {}
        for actor in query_actors:
            actors[actor.id] = actor.name
        return jsonify({
            'Actors': actors
        }), 200
    
    #Delete Movie
    @app.route('/movies/<int:m_id>', methods=['DELETE'])
    def del_movie(m_id):
        try:
            movie = Movies.query.filter(Movies.id == m_id).one_or_none()
            movie.delete()
            return jsonify({
                'success': True
            })
        except BaseException:
            abort(404)
        return jsonify({
            'status': 'Deleted Successful'
        }), 200
        
    #Insert MOvie
    @app.route('/movies', methods=['POST'])
    def post_movie():
        body = request.get_json()
        name = body.get('name')
        actor = body.get('actor')
        try:
            movie = Movies(
                name = name,
                actor = actor
            )
            Movies.insert(movie)
        except BaseException:
            return jsonify({
                'status': 'new movie failed!'
            })
        return jsonify({
            'status': 'Successfully added a movie',
            'success': True
        }), 201

    #Insert Actor
    @app.route('/actors', methods=['POST'])
    def post_actor():
        body = request.get_json()
        name = body.get('name')
        try:
            actor = Actors(
                name = name
            )
            Actors.insert(actor)
        except BaseException:
            return jsonify({
                'status': 'new actor failed!'
            })
        return jsonify({
            'status': 'Successfully added a actor',
            'success': True
        }), 201
    '''
    Error Handlers
    '''
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            'message': 'resource not found!',
            'success': False}), 404

    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({
            'message': 'method NOT allowed!'
            }), 405

    return app
    


