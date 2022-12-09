from flask import Flask
from pymongo import MongoClient

from controller import routes

import certifi

ca=certifi.where()

SECRET_KEY = 'SPARTA'

import jwt

import datetime

import hashlib

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
