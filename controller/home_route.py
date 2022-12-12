import os

import jwt
from dotenv import load_dotenv

from flask import render_template, request
from . import routes

from pymongo import MongoClient

SECRET_KEY = 'SPARTA'

load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/')
def home():
    return render_template('home_login.html')

@routes.route('/accept')
def home_accept():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.member.find_one({"id": payload['id']})
        return render_template('home.html', nickname=user_info["nickname"])
    except:
        return render_template('home.html')



