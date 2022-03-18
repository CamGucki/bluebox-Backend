from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_cors import CORS, cross_origin
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')


db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    movieImg = db.Column(db.String )
    category = db.Column(db.String)



    def __init__(self,title, description, movieImg, category):
        self.title = title
        self.description = description
        self.movieImg = movieImg
        self.category = category
class MovieSchema(ma.Schema):
    class Meta:
        fields = ('title', 'description','movieImg', 'category')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many = True)

@app.route('/')
def index():
    return '<div> Hello World! <div>'


@app.route('/movie', methods = ['POST'])
def create_movie():
    
    title = request.json['title']
    description = request.json['description']
    movieImg = request.json['movieImg']
    category = request.json['category']

    new_movie = Movie(title,description,movieImg,category)
 
    db.session.add(new_movie)
    db.session.commit()

    return movie_schema.jsonify(new_movie)



@app.route('/movies', methods = ['GET'])
def get_movies():

    movies = Movie.query.all()
    result = movies_schema.dump(movies)
    
    return jsonify(result)

#  End point to get all movies


@app.route('/movie/<id>', methods = ['GET'])
def get_movie(id):

    movie  = Movie.query.get(id)

    return movie_schema.jsonify(movie)

#  End point to get a movie

@app.route('/movie/<id>', methods = ['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)

    title = request.json['title']
    description = request.json['description']
    movieImg = request.json['movieImg']
    category= request.json['category']

    movie.title = title
    movie.description = description
    movie.movieImg = movieImg
    movie.category= category
    db.session.commit()

    return movie_schema.jsonify(movie)


@app.route("/movie/<id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)
    
    db.session.delete(movie)
    db.session.commit()

    return movie_schema.jsonify(movie)

#  End point for deleting a movie

if __name__ == '__main__':
    app.run(debug = True)