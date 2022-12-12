import os
from dotenv import load_dotenv
from pymongo import MongoClient

from flask import render_template, request, jsonify
from . import routes

import hashlib
import datetime
import jwt

# #Flask-Mail
# from flask import Flask
# from flask_mail import Mail, Message
#
# app = Flask(__name__)
# mail = Mail(app)
# print('555555555555555555555555555')
# print(app.config)
# print(mail)
# print('555555555555555555555555555')



load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
SECRET_KEY = os.environ.get('SECRET_KEY')
client = MongoClient(mySecretKey)
db = client.worldcup


@routes.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@routes.route('/api/login', methods=['POST'])
def api_login():
    all_members = list(db.member.find({}, {'_id': False}))

    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() # 암호화??

    result = db.member.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'pw': pw_hash
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# @routes.route('/test')
# def test():
#     app.config['MAIL_SERVER'] = 'smtp.gmail.com'
#     app.config['MAIL_PORT'] = 465
#     app.config['MAIL_USERNAME'] = 'silve45345@gmail.com'
#     app.config['MAIL_PASSWORD'] = 'pqqx burn xcup afir'
#     app.config['MAIL_USE_TLS'] = False
#     app.config['MAIL_USE_SSL'] = True
#     mail = Mail(app)
#
#     print('666666666666666666666')
#     print(app.config)
#     print(mail)
#     print('666666666666666666666666')
#
#     msg = Message('Hello_world_34124123421', sender='silve45345@gmail.com', recipients=['dirn0568@naver.com'])
#     msg.body = 'Hello Flask 메세지에용'
#     mail.send(msg)
#     return 'Sent'



