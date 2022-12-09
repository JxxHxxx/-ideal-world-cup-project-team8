from flask import Flask
from pymongo import MongoClient

from controller import routes

client = MongoClient('mongodb+srv://test:1gPwls4189@cluster0.jhc3fyv.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.worldcup

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
