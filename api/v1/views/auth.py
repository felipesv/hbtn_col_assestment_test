#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from app import mysql


@app_views.route('/login/', methods=['POST'], strict_slashes=False)
def login():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT count(*) FROM users''')
    data = cur.fetchall()
    print(data)
    return jsonify("TEST")
