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
    price = db.Column(db.Integer)
    belongsTo = db.Column(db.Integer)
    movieImg = db.Column(db.String )



    def __init__(self,title, description,price,belongsTo, movieImg):
        self.title = title
        self.description = description
        self.price = price
        self.belongsTo = belongsTo
        self.movieImg = movieImg

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('title', 'description','price','belongsTo', 'movieImg')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many = True)

@app.route('/')
def index():
    return '<div> Hello World! <div>'


@app.route('/movie', methods = ['POST'])
def create_movie():
    
    title = request.json['title']
    description = request.json['description']
    price = request.json['price']
    belongsTo = request.json['belongsTo']
    movieImg = request.json['movieImg']

    new_movie = Movie(title,description,price, belongsTo, movieImg)
 
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
    price = request.json['price']
    belongsTo = request.json['belongsTo']
    movieImg = request.json['movieImg']

    movie.title = title
    movie.description = description
    movie.price = price
    movie.belongsTo = belongsTo
    movie.movieImg = movieImg

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