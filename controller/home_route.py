import os

import jwt
from dotenv import load_dotenv

from flask import render_template, request, redirect, url_for
from . import routes

from pymongo import MongoClient

SECRET_KEY = 'SPARTA'

load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.member.find_one({"id": payload['id']})
        return render_template('home.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

