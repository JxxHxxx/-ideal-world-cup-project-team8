import hashlib
import os

import jwt
from dotenv import load_dotenv

from flask import render_template, request, redirect, url_for, jsonify
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
        user_info = db.member.find_one({'id': payload['id'], "pw": payload['pw']})
        if user_info != None:
            return redirect(url_for('routes.home_accept'))
    except:
        return render_template('home_login.html')

@routes.route('/accept')
def home_accept():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.member.find_one({'id': payload['id'], "pw": payload['pw']})
        if user_info == None:
            return redirect(url_for('routes.home'))
        return render_template('home.html', nickname=user_info["nickname"])
    except:
        return redirect(url_for('routes.home'))



