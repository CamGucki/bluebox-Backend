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
   name = db.Column(db.String)
   email = db.Column(db.String, unique = True)
   password = db.Column(db.String)
   

   def __init__(self,name, email, password):
       self.name = name
       self.email = email
       self.password = password
       

class UserSchema(ma.Schema):
        class Meta:
            fields = ('name','email', 'password',)

user_schema = UserSchema()
users_schema = UserSchema(many = True)

@app.route('/')
def index():
    return '<div>USERS</div>'

#endpoint to register

@app.route ('/user', methods =['POST'])
def create_user():
    data = request.json.get('user')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    


    new_user = User (name , email, password)

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

    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    rating = request.json ['rating']
    
    user.name = name
    user.email = email
    user.password = password
    user.rating = rating 

    db.session.commit()

    return user_schema.jsonify(user)


#  End point for deleting a movie

if __name__ == '__main__':
    app.run(debug = True)

