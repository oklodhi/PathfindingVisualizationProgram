from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return "<h1>Auth Test</h1>"