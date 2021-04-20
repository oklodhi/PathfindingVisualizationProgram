from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'u\xbb\xa3\x08\x12\xbc"\xf9\xd9X\\\x02\x9d\xebk^\x14\x98b\xa6YUl\x1a'

    return app

