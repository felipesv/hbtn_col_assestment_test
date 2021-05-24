#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from app import mysql


@app_views.route('/orders/', methods=['GET'], strict_slashes=False)
def get_orders():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT count(*) FROM users''')
    data = cur.fetchall()
    return jsonify("TEST")
