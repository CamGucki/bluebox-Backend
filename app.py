from flask import Flask
from sqlalchemy import true

app = Flask(__name__)

@app.route('/movies')
def hello ():
    return "hey flask"

if __name__=='__main__':
    app.run(debug = True)
