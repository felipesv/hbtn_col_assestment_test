from routes import *
from flask import Flask, Blueprint

app = Flask(__name__)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.secret_key = 'asfg3442dsq'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=8000, threaded=True, debug=True)
