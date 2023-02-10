import os
import re

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from controller import routes

import hashlib
import certifi

import random

load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_PASSWORD = os.environ.get('SECRET_PASSWORD')
client = MongoClient(mySecretKey)
db = client.worldcup

#Flask-Mail
from flask_mail import Mail, Message

ca=certifi.where()

app = Flask(__name__)
app.register_blueprint(routes)

#Flask-Mail
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'silve45345@gmail.com'
app.config['MAIL_PASSWORD'] = SECRET_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/pw_find')
def pw_find():
    all_users = list(db.member.find({}, {'_id': False}))
    print(all_users)
    # a = 'dirn0568@naver.com'
    #
    # code = random.randint(100000, 999999)
    #
    # msg = Message('비밀번호 코드', sender='silve45345@gmail.com', recipients=[a])
    # msg.body = '인증코드 : {0}'.format(code)
    # mail.send(msg)
    return render_template('home_pw_find.html')

@app.route('/api/pw_find', methods=['POST'])
def api_pw_find():
    id_receive = request.form['id_give']
    code_receive = request.form['code_give']
    pw_receive = request.form['pw_give']
    pw_re_receive = request.form['pw_re_give']

    if id_receive != "" and code_receive == "" and pw_receive == "" and pw_re_receive == "":
        result = db.member.find_one({'id': id_receive})
        print("result :", result)

        if result is not None:
            email_receive = result['email']

            code = random.randint(100000, 999999)

            db.member.update_one({'id': id_receive}, {'$set': {'code': code}})

            msg = Message('비밀번호 코드', sender='silve45345@gmail.com', recipients=[email_receive])
            msg.body = '인증코드 : {0}'.format(code)
            mail.send(msg)
            return jsonify({'result': 'success1'})
        else:
            return jsonify({'result': 'fail1'})
    elif id_receive != "" and code_receive != "" and pw_receive == "" and pw_re_receive == "":
        result = db.member.find_one({'id': id_receive})
        print("3 :", result)
        print(code_receive)
        print(type(code_receive))
        print(result['code'])
        print(type(result['code']))
        if result is not None:
            if int(code_receive) == result['code']:
                return jsonify({'result': 'success2'})
            else:
                return jsonify({'result': 'fail2'})
        else:
            return jsonify({'result': 'fail2'})
    elif id_receive != "" and code_receive != "" and pw_receive != "" and pw_re_receive == "":
        result = db.member.find_one({'id': id_receive})

        reg_pw = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,20}$'

        if not re.search(reg_pw, pw_receive):
            result = 'fail3'
            return jsonify({'result': result})
        return jsonify({'result': 'success3'})
    elif id_receive != "" and code_receive != "" and pw_receive != "" and pw_re_receive != "":
        print("4단계 실행중>>>>")
        print(id_receive)
        print(code_receive)
        print(pw_receive)
        print(pw_re_receive)
        print("4단계 실행중>>>>")
        result = db.member.find_one({'id': id_receive})
        print("result:", result)
        reg_pw = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,20}$'

        if not re.search(reg_pw, pw_re_receive):
            print("정규식 실행중????")
            result = 'fail4'
            return jsonify({'result': result})

        if pw_receive != pw_re_receive:
            print("일치하지않음")
            result = 'fail4'
            return jsonify({'result': result})

        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()  # 암호화??
        db.member.update_one({'id': id_receive}, {'$set': {'pw': pw_hash}})
    # code = random.randint(100000, 999999)
    #
    # msg = Message('비밀번호 코드', sender='silve45345@gmail.com', recipients=[id_receive])
    # msg.body = '인증코드 : {0}'.format(code)
    # mail.send(msg)
    return jsonify({'result': 'success4'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
