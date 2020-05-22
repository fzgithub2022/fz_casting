import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

'''
database_name = "capdb"
database_uname = "postgres"
database_password = "pgpw"
database_path = "postgres://{}:{}@{}/{}".format(database_uname,database_password,'localhost:5432', database_name)
'''

DATABASE_URL = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL #database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Movies
'''
class Movies(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    rdate = Column(String)

    def __init__(self, name, rdate):
        self.name = name
        self.rdate = rdate
    
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
            'rdate': self.rdate
        }



'''
Actors
'''
class Actors(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    
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
            'gender': self.gender
        }