import os

from dotenv import load_dotenv
from flask import render_template, jsonify
from pymongo import MongoClient

from . import routes

load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/api/select', methods=['GET'])
def show_noddle():

    noodle_list = list(db.noodle.find({}, {"_id": False}))

    return jsonify({'ideal': noodle_list})

@routes.route('/select', methods=['get'])
def select():
    return render_template('idealSelect.html')