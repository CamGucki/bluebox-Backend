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

class User(db.Model):

   id = db.Column(db.Integer, primary_key = True)
   email = db.Column(db.String)
   password = db.Column(db.String)
   streetAddress = db.Column(db.String)
   state = db.Column(db.String)
   city = db.Column(db.String)
   zip = db.Column(db.Integer)

   def __init__(self, email, password, streetAddress,city,zip, state):
       self.email = email
       self.password = password
       self.streetAddress = streetAddress
       self.city = city
       self.zip = zip
       self.state = state

class UserSchema(ma.Schema):
        class Meta:
            fields = ('email', 'password', 'streetAddress','city','zip', 'state')

user_schema = UserSchema()
users_schema = UserSchema(many = True)

@app.route('/')
def index():
    return '<div>USERS</div>'

#endpoint to register

@app.route ('/user', methods =['POST'])
def create_user():

    email = request.json['email']
    password = request.json['password']
    streetAddress = request.json['streetAddress']
    city = request.json['city']
    state = request.json['state']
    zip = request.json['zip']

    new_user = User('email', 'password', 'streetAddress','city','zip')

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


#endpoint to get user

@app.route ('/user/<id>', methods =['GET'])
def get_user():

    email = request.json['email']
    password = request.json['password']
    streetAddress = request.json['streetAddress']
    city = request.json['city']
    state = request.json['state']
    zip = request.json['zip']

    new_user = User('email', 'password', 'streetAddress','city','zip')

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)
    
#to get all users
@app.route('/users', methods = ['GET'])
def get_users():

    users = User.query.all()
    result = users_schema.dump(users)
    
    return jsonify(result)


#to get one user

@app.route('/user/<id>', methods = ['GET'])
def get_user(id):

    user  = User.query.get(id)

    return user_schema.jsonify(user)

@app.route('/user/<id>', methods = ['PUT'])
def update_user(id):
    user = user.query.get(id)

    email = request.json['email']
    password = request.json['password']
    streetAddress = request.json['streetAddress']
    city = request.json['city']
    state = request.json['state']
    zip = request.json['zip']

    user.email = email
    user.password = password
    user.streetAddress = streetAddress
    user.city = city
    user.zip = zip

    db.session.commit()

    return user_schema.jsonify(user)


#  End point for deleting a movie

if __name__ == '__main__':
    app.run(debug = True)

