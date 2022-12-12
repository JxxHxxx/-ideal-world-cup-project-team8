import os

import jwt
from dotenv import load_dotenv

from flask import render_template, request, redirect, url_for
from . import routes

from pymongo import MongoClient


load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
SECRET_KEY = os.environ.get('SECRET_KEY')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.member.find_one({"id": payload['id']})
        return render_template('home.html', nickname=user_info["nickname"])
    except:
        return render_template('home.html')


