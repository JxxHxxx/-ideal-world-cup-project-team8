import os

import js as js
from dotenv import load_dotenv
from flask import render_template, request, jsonify
from pymongo import MongoClient

import jwt
import hashlib
import datetime

SECRET_KEY = 'SPARTA'

from . import routes


load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/sign', methods=['GET'])
def members():
    return render_template('/sign_register.html')


@routes.route("/members", methods=["POST"])
def members_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    doc = {
        'id': id_receive,
        'pw': pw_receive,
        'nickname': nickname_receive
    }

    db.member.insert_one(doc)

    return jsonify({'msg': '주문 완료!'})

@routes.route("/members", methods=["GET"])
def members_get():
    orders_list = list(db.orders.find({},{'_id':False}))
    return jsonify({'orders':orders_list})


@routes.route('/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})


    if result is not None:

        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')


        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

    if __name__ == '__main__':
        app.run('0.0.0.0', port=5000, debug=True)