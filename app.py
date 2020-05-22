from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import json
from flask_migrate import Migrate
from models import setup_db, Movies, Actors, db, os

#create and configure the app
app = Flask(__name__)
#setup_db(app) #connect to databse and models

#migrate = Migrate(app, db)

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

#Route decorator
@app.route('/')
def route_decorator():
    return jsonify({
        "success": True,
        "status": 'App is running!',
        "database": os.environ['DATABASE_URL']
    })

#Get Movies Decorator
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movies.query.all()
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
        'movies': formatted_movies
    }), 200

#Get Actors Decorator
@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actors.query.all()
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
        'Actors': formatted_actors
    }), 200

#Delete Movie
@app.route('/movies/<int:m_id>', methods=['DELETE'])
def del_movie(m_id):
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
def del_actor(a_id):
    try:
        actor = Actors.query.filter(Actors.id == a_id).one_or_none()
        actor.delete()
    except BaseException:
        abort(404)
    return jsonify({
        'status': 'Deleted Successful'
    }), 200
    
#Insert Movie
@app.route('/movies', methods=['POST'])
def post_movie():
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
        return jsonify({
            'status': 'new actor failed!'
        })
    return jsonify({
        'status': 'Successfully added a actor',
        'success': True
    }), 201

#Patch movie
@app.route('/movies/<int:m_id>', methods=['PATCH'])
def patch_movie(m_id):
    body = request.get_json()
    try:
        movie = Movies.query.filter(Movies.id == m_id).one_or_none()
        if movie is None:
            abort(404)
    except BaseException:
        abort(404)
    rdate = body.get('rdate')
    if rdate is not None:
        movie.rdate = rdate
    Movies.update(movie)
    return jsonify ({
        "status": "Move updated",
        "success": True
    })

#Patch Actor
@app.route('/actors/<int:a_id>', methods=['PATCH'])
def patch_actor(a_id):
    body = request.get_json()
    try:
        actor = Actors.query.filter(Actors.id == a_id).one_or_none()
        if actor is None:
            abort(404)
    except BaseException:
            abort(404)
    age = body.get('age')
    if age is None:
        abort(400)
    actor.age = age
    gender = body.get('gender')
    if gender is None:
        abort(400)
    actor.gender = gender
    Actors.update(actor)
    return jsonify({
        "status": "Actor updated successfully",
        "success": True
    })


'''
Error Handlers
'''
@app.errorhandler(400)
def handle_400(error):
    return jsonify({
        'message': 'bad request! shame on you',
        'success': 'False'
    }), 400

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
    


