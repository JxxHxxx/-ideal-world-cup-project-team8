import os

from dotenv import load_dotenv
from flask import Flask
from pymongo import MongoClient

from controller import routes

load_dotenv()

mySecretKey = os.environ.get('MySecretKey')
client = MongoClient(mySecretKey)
db = client.worldcup

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
