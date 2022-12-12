import os

from dotenv import load_dotenv
from flask import render_template, jsonify, request, redirect, url_for
import jwt
from pymongo import MongoClient

from . import routes

load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/select', methods=['GET'])
def select():
    return render_template('idealSelect.html')

@routes.route('/api/noodle/read', methods=['GET'])
def read_noddle():
    noodle_list = list(db.noodle.find({}, {"_id": False}))
    noodle_list = sorted(noodle_list, key=lambda noodle_list: noodle_list['win'], reverse=True)

    return jsonify({'ideal': noodle_list})

JWT_SECRET_KEY = "SPARTA"
@routes.route('/api/nick', methods=['GET'])
def get_cookies():
    token = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        login_member = db.member.find_one({'id': payload['id']})

        return login_member['nickname']

    except jwt.ExpiredSignatureError:
        return redirect(url_for("routes.get_cookies", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("routes.get_cookies", msg="로그인 정보가 존재하지 않습니다."))

@routes.route('/select/result', methods=['GET'])
def result():
    return render_template('result.html')

@routes.route('/api/noodle/save', methods=['POST'])
def save_result():
    img_receive = request.form['img_give']
    find_noodle = db.noodle.find_one({'img': img_receive})

    db.noodle.update_one({'img': img_receive}, {'$set': {'win': find_noodle['win'] + 1}})
    db.noodle.update_one({'img': img_receive}, {'$push':{'nicknames': login_member['nickname']}})
    return "ok"