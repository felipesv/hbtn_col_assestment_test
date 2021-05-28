#!/usr/bin/python3
from api.v1.views import app_views
from flask import json, jsonify, request, abort
from app import mysql
import jwt


def valid_token(encoded_jwt):
    try:
        payload = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user_id = payload.get("id")
        sql = "SELECT * FROM users WHERE user_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(sql, (user_id, ))
        data = cur.fetchall()
        if (not data):
            raise Exception
        return True
    except:
        return False


def getid_token(encoded_jwt):
    try:
        payload = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user_id = payload.get("id")
        return user_id
    except:
        return None


def mysql_run(sql, data_in, insert=False):
    # EXECUTE QUERY
    cur = mysql.connection.cursor()
    cur.execute(sql, data_in)
    data = cur.fetchall()
    # VALID DATA
    num_fields = len(data)
    if num_fields == 0 and not insert:
        raise Exception
    return data


def dict_user(order):
    return {
        "first_name": order[0],
        "last_name": order[1],
        "email": order[2],
        "gov_id": order[3],
        "company": order[4],
    }


@app_views.route('/users/all', methods=['GET'], strict_slashes=False)
def get_all_users():
    try:
        results = []
        # VALID TOKEN
        token = request.headers.get('x-auth-token')
        if not valid_token(token):
            return jsonify({"message": "Unauthorized"}), 401
        # QUERY
        sql = "SELECT user_name, user_last_name, user_email, user_gov_id, user_company \
            FROM users"
        data = mysql_run(sql, None)
        # FETCH RESULT
        for val in data:
            user = dict_user(val)
            results.append(user)
        return jsonify(results)
    except:
        return jsonify({"message": "Orders not found"}), 404
