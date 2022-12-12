import os

from dotenv import load_dotenv
from flask import render_template, jsonify, request, redirect, url_for
import jwt
from pymongo import MongoClient

from . import routes
SECRET_KEY = 'SPARTA'
load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/api/noodle', methods=['GET'])
def read_noodle():
    noodle_list = list(db.noodle.find({}, {"_id": False}))
    noodle_list = sorted(noodle_list, key=lambda noodle_list: noodle_list['win'], reverse=True)

    return jsonify({'ideal': noodle_list})

JWT_SECRET_KEY = "SPARTA"
@routes.route('/api/nick', methods=['GET'])
def read_nickname():
    token = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        login_member = db.member.find_one({'id': payload['id']})

        return login_member['nickname']

    except jwt.ExpiredSignatureError:
        return redirect(url_for("routes.get_cookies", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("routes.get_cookies", msg="로그인 정보가 존재하지 않습니다."))

@routes.route('/api/noodle/save', methods=['POST'])
def save_result():
    token = request.cookies.get("mytoken")
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
    login_member = db.member.find_one({'id': payload['id']})

    img_receive = request.form['img_give']
    find_noodle = db.noodle.find_one({'img': img_receive})

    db.noodle.update_one({'img': img_receive}, {'$set': {'win': find_noodle['win'] + 1}})
    db.noodle.update_one({'img': img_receive}, {'$push':{'nicknames': login_member['nickname']}})
    return "ok"

@routes.route('/play/results', methods=['GET'])
def result():
    token = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        db.member.find_one({'id': payload['id']})
        return render_template('result.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("routes.home", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("routes.home", msg="로그인 정보가 존재하지 않습니다."))

@routes.route('/play', methods=['GET'])
def select():
    token = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        db.member.find_one({'id': payload['id']})
        return render_template('idealSelect.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("routes.home", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("routes.home", msg="로그인 정보가 존재하지 않습니다."))

@routes.route('/play/result/<noodle_name>', methods=['GET'])
def detail(noodle_name):
    find_noodle = db.noodle.find_one({'name': noodle_name})

    token = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        db.member.find_one({'id': payload['id']})
        return render_template('detail.html', nickname_list=find_noodle['nicknames'], noodle_name = noodle_name)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("routes.home", msg="로그인 시간이 만료되었습니다."))

    except jwt.exceptions.DecodeError:
        return redirect(url_for("routes.home", msg="로그인 정보가 존재하지 않습니다."))

