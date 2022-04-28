from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
from flask_cors import CORS, cross_origin
import os
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
import datetime


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY']= 'thisissecret'

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

# class User (db.Model):
#     id= db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String, unique=True)
#     name = db.Column(db.String)
#     password= db.Column(db.String)
#     admin= db.Column(db.Boolean)

# @app.route('/user', methods=['GET'])
# def get_all_users():
#     users = User.query.all()
#     output = []

#     for user in users:
#         user_data = {}
#         user_data['public_id'] = user.public_id
#         user_data['name'] = user.name
#         user_data['password'] = user.password
#         user_data['admin'] = user.admin
#         output.append(user_data)

#     return jsonify({'users': output})

# @app.route('/user/<user_id>', methods=['GET'])
# def get_one_user(public_id):

#     user=User.query.filter_by(public_id=public_id).first()

#     if not user:
#         return jsonify({'message': 'No User found!'})

#     user_data = {}
#     user_data['public_id'] = user.public_id
#     user_data['name'] = user.name
#     user_data['password'] = user.password
#     user_data['admin'] = user.admin

#     return jsonify({'user': 'user_data'})

# @app.route('/user', methods=['POST'])
# def create_user():

#     data= request.get_json()

#     hashed_password = generate_password_hash(data['password'], method='sha256')

#     new_user = User(public_id=str(uuid.uuid4()), name = data['name'], password = hashed_password, admin=False)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'New user created'})



# @app.route('/user/<public_id>' , methods=['PUT'])
# def promote_user(public_id):

#     user=User.query.filter_by(public_id=public_id).first()
    

#     if not user:
#         return jsonify({'message': 'No User found!'})

#     user.admin = True
#     db.session.commit()
#     return jsonify({'message': ' The user has been promoted!' })

# @app.route('/user/<public_id>', methods=['DELETE'])
# def delete_user(public_id):

#     user=User.query.filter_by(public_id=public_id).first()
    

#     if not user:
#         return jsonify({'message': 'No User found!'})

#     db.session.delete(user)
#     db.session.commit()

#     return jsonify({'message': 'The user has beeen deleted'})



# @app.route('/login')
# def login():
#     auth= request.authorization

#     if not auth or not auth.username or not auth.password:
#         return make_response('could not verify', 401, {' WWW-Authencicate': 'Basic realm= "login required!"'})

#     user = User.query.filter_by(name=auth.username).first()

#     if not user :
#         return make_response('could not verify', 401, {' WWW-Authencicate': 'Basic realm= "login required!"'})

#     if check_password_hash(user.password, auth.password):
#         token= jwt.encode({'public_id': user.public_id, 'exp':datetime.datetime.utcnow()+ datetime.timedelta(minutes=30) }, app.config['SECRET_KEY'])

#         return jsonify ({'token': token.decode('UTF-8')})

#     return make_response('could not verify', 401, {' WWW-Authencicate': 'Basic realm= "login required!"'})






class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    movieImg = db.Column(db.String )
    category = db.Column(db.String)
    ratingValue = db.Column(db.Integer, nullable=True)
  
#sqlalchemy how to define NOT NULL

    def __init__(self, title, description, movieImg, category, ratingValue):
        self.title = title
        self.description = description
        self.movieImg = movieImg
        self.category = category
        self.ratingValue = ratingValue
        
        


class MovieSchema(ma.Schema):
    class Meta:
        fields = ('title', 'description','movieImg', 'category','ratingValue','id')


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
    ratingValue = request.json['ratingValue']
    new_movie = Movie(title,description,movieImg,category,ratingValue)
 
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

    ratingValue = request.json['ratingValue']
    movie.ratingValue = ratingValue
    
    
    db.session.commit()
    return movie_schema.jsonify(movie)


@app.route("/movie/<id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)
    
    db.session.delete(movie)
    db.session.commit()
    return movie_schema.jsonify(movie)
    
if __name__ == '__main__':
    app.run(debug = True)