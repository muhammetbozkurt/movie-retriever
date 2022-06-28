from flask import Flask, request
from api import MovieRetriever

app = Flask(__name__)
  
@app.route('/test', methods = ['GET'])
def disp():
    args = request.args
    print (args) # For debugging
    df = MovieRetriever.retrieve_movies(**args)
    return df.to_json()


if __name__ == '__main__':
  
    app.run(debug = True)