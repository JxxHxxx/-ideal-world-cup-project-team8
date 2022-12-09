import os

from dotenv import load_dotenv
from flask import render_template
from pymongo import MongoClient

from . import routes
load_dotenv()
mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

@routes.route('/sign', methods=['GET'])
def sign_get():
    return render_template('/sign.html')


