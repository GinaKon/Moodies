from flask import Flask, jsonify, request
from main import MatchMood

app = Flask(__name__)

@app.route('/hello', methods = ["GET"]) #www.google.com
def helloworld():
    if request.method == "GET":  
      return {'Hello':'World'}
