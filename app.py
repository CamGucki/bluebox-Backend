from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow (app)

class Movies(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String (100), unique = False)
    description = db.Column (db.String(3000), unique = False)

    def __init__(self, title, description):
        self.title = title
        self.description= description

class MovieSchema(ma.Schema):
    class Meta: 
        fields = ('title','description') 

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

if __name__=='__main__':
    app.run(debug = True)
