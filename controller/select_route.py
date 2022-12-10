import os

from dotenv import load_dotenv
from flask import render_template, jsonify, request
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

@routes.route('/select/result', methods=['GET'])
def result():
    return render_template('result.html')

@routes.route('/api/noodle/save', methods=['POST'])
def save_result():
    img_receive = request.form['img_give']
    find_noodle = db.noodle.find_one({'img': img_receive})

    db.noodle.update_one({'img': img_receive}, {'$set': {'win': find_noodle['win'] + 1}})
    return "ok"