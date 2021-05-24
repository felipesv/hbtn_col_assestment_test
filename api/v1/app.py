#!/usr/bin/python3
"""
Flask Application
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from os import environ

app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'hbtn_orders'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'orders'

mysql = MySQL(app)

@app.errorhandler(404)
def not_found(error):
    """ 404 Not Found"""
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    """
    Main funtion
    """
    host = environ.get('ORDER_API_HOST')
    port = environ.get('ORDER_API_PORT')

    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True, debug=True)
