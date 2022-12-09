from flask import render_template
from . import routes

@routes.route('/sign', methods=['GET'])
def sign_get():
    return render_template('/sign.html')


