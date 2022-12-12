import hashlib
import os
import re

from dotenv import load_dotenv

from flask import render_template, request, jsonify
from pymongo import MongoClient

from . import routes

SECRET_KEY = 'SPARTA'

load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/sign', methods=['GET'])
def sign_get():
    all_members = list(db.member.find({}, {'_id': False}))
    print("----------------")
    print(all_members)
    print("----------------")
    return render_template('/sign.html')

@routes.route('/api/sign', methods=['POST'])
def api_sign():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_re_receive = request.form['pw_re_give']
    nick_receive = request.form['nick_give']

    reg_id = r'^[A-Za-z0-9_]{4,15}$'

    if not re.search(reg_id, id_receive):
        result = 'fail_reg'
        return jsonify({'result': result})

    member_check = db.member.find_one({'id': id_receive})

    if member_check == None:
        result = 'success'
    else:
        result = 'fail_re'
        return jsonify({'result': result})

    if not pw_receive == pw_re_receive:
        result = 'fail_re'
        return jsonify({'result': result})

    reg_pw = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,20}$'

    if not re.search(reg_pw, pw_receive):
        result = 'fail_reg'
        return jsonify({'result': result})

    reg_nick = r'^[A-Za-zㄱ-ㅣ가-힣0-9]{2,10}$'

    if not re.search(reg_nick, nick_receive):
        result = 'fail_reg'
        return jsonify({'result': result})

    member_check = db.member.find_one({'nickname': nick_receive})

    if member_check == None:
        result = 'success'
    else:
        result = 'fail_re'
        return jsonify({'result': result})

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() # 암호화??
    print("=============================")
    print(id_receive)
    print(pw_hash)
    print(nick_receive)
    print("=============================")
    db.member.insert_one({'id': id_receive, 'pw': pw_hash, 'nickname': nick_receive})

    return jsonify({'result': 'success'})

@routes.route('/api/id_check', methods=['POST'])
def api_id_check():
    id_receive = request.form['id_give']

    reg = r'^[A-Za-z0-9_]{4,15}$'

    if not re.search(reg, id_receive):
        result = 'fail_reg'
        return jsonify({'result': result})

    member_check = db.member.find_one({'id': id_receive})

    if member_check == None:
        result = 'success'
    else:
        result = 'fail_re'
    return jsonify({'result': result})

@routes.route('/api/nick_check', methods=['POST'])
def api_nick_check():
    nick_receive = request.form['nick_give']
    print(nick_receive)

    nick_data = nick_receive
    reg = r'^[A-Za-zㄱ-ㅣ가-힣0-9]{2,10}$'

    if not re.search(reg, nick_data):
        result = 'fail_reg'
        return jsonify({'result': result})

    member_check = db.member.find_one({'nickname': nick_receive})
    print(member_check)

    if member_check == None:
        result = 'success'
    else:
        result = 'fail_re'
    return jsonify({'result': result})
