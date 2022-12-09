from flask import render_template
from . import routes

@routes.route('/login', methods=['GET'])
def login():
    return render_template('login.html')










