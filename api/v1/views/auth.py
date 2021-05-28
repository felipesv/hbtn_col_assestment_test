#!/usr/bin/python3
from api.v1.views import app_views
from app import mysql
from flask import json, jsonify, request, abort
from flask_mysqldb import MySQL
import jwt
import uuid


@app_views.route('/signup/', methods=['POST'], strict_slashes=False)
def signup():
    try:
        args = request.get_json()
        if args is None:
            return jsonify({"error": "Not a JSON"}), 400

        user_id = uuid.uuid4()
        sql = "INSERT INTO users(user_id, user_name, user_last_name, user_gov_id, \
            user_email, user_company, user_password) \
            VALUES(%s, %s, %s, %s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(sql, (user_id, args.get("first_name"),
                    args.get("last_name"),
                    args.get("gov_id"), args.get("email"),
                    args.get("company"), args.get("password")))
        mysql.connection.commit()
        return jsonify({"message": "User registered"})
    except:
        return jsonify({"message": "The email registered already exists"}), 400


@app_views.route('/login/', methods=['POST'], strict_slashes=False)
def signin():
    try:
        args = request.get_json()
        sql = "SELECT user_id FROM users WHERE user_email = %s AND \
            user_password = %s"
        cur = mysql.connection.cursor()
        cur.execute(sql, (args.get("email"), args.get("password")))
        data = cur.fetchall()
        if (not data):
            raise Exception

        user_id = data[0][0]
        encoded_jwt = jwt.encode({"id": user_id}, "secret",
                                 algorithm="HS256")
        return jsonify({"api_key": encoded_jwt})
    except:
        return jsonify({"message": "User not found"}), 404
