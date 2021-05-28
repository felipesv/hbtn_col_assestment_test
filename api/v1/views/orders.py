#!/usr/bin/python3
from api.v1.views import app_views
from flask import json, jsonify, request, abort
from app import mysql
import datetime
import jwt
import random
import sys
import uuid


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


def dict_order(order):
    return {
        "order_id": order[0],
        "order_date": order[1],
        "order_subtotal": '$' + str(order[2]),
        "order_taxes": '$' + str(order[3]),
        "order_total": '$' + str(order[4]),
        "order_status": "Paid" if order[5] == 1 else "Not paid",
        "gov_id": order[6],
        "customer_id": order[7],
        "company": order[8],
        "customer_name": order[9],
        "last_payment_date": order[10],
        "payment_type": order[11],
        "payment_status": order[12],
        "payment_txn_id": order[13],
        "payment_total": '$' + str(order[14]),
        "shipping_address": order[15],
        "shipping_city": order[16],
        "shipping_state": order[17],
        "shipping_country": order[18],
        "shipping_cost": '$' + str(order[19]),
    }


@app_views.route('/orders/<orderid>', methods=['GET'], strict_slashes=False)
def get_order_by_id(orderid):
    try:
        results = []
        # VALID TOKEN
        token = request.headers.get('x-auth-token')
        if not valid_token(token):
            return jsonify({"message": "Unauthorized"}), 401
        # MULTI IDS
        orders_id = orderid.split(',')
        for order_id in orders_id:
            # QUERY
            sql = "SELECT a.order_id, a.orders_date, a.orders_subtotal, a.orders_taxes, \
                    a.orders_total, a.orders_paid, b.user_gov_id, b.user_id, \
                    b.user_company, CONCAT(b.user_name,' ',b.user_last_name), \
                    c.payment_date, c.payment_type, c.payment_status, \
                    c.payment_txn_id, c.payment_total, d.shipping_address, \
                    d.shipping_city, d.shipping_state, d.shipping_country, \
                    d.shipping_cost \
                    FROM orders AS a \
                    INNER JOIN users AS b \
                    ON a.user_id = b.user_id \
                    INNER JOIN payment AS c \
                    ON a.order_id = c.order_id \
                    INNER JOIN shipping AS d \
                    ON a.order_id = d.order_id \
                    WHERE a.order_id = %s"
            data = mysql_run(sql, (order_id,))
            # FETCH RESULT
            for val in data:
                order = dict_order(val)
                results.append(order)
        if len(orders_id) == 1:
            return jsonify(results[0])
        return jsonify(results)
    except:
        return jsonify({"message": "Order not found"}), 404


@app_views.route('/orders/<date1>/<date2>', methods=['GET'],
                 strict_slashes=False)
def order_by_dates(date1, date2):
    try:
        results = []
        # VALID TOKEN
        token = request.headers.get('x-auth-token')
        if not valid_token(token):
            return jsonify({"message": "Unauthorized"}), 401
        # QUERY
        sql = "SELECT order_id from orders WHERE orders_date between %s AND %s"
        data = mysql_run(sql, (date1, date2))
        # FETCH RESULT
        for val in data:
            results.append(val[0])
        return jsonify(results)
    except:
        return jsonify({"message": "Orders not found"}), 404


@app_views.route('/orders/shipping/', methods=['GET'],
                 strict_slashes=False)
def orders_by_shipping_key():
    try:
        results = []
        # VALID TOKEN
        token = request.headers.get('x-auth-token')
        if not valid_token(token):
            return jsonify({"message": "Unauthorized"}), 401
        # PARAMS
        k_arg = request.args.keys()
        if len(k_arg) != 1 and k_arg not in ['city', 'state', 'country']:
            return jsonify({"message": "Bad request"}), 400
        c_name = list(k_arg)[0]
        value = request.args.get(c_name)
        # QUERY
        sql = "SELECT a.order_id, a.orders_date, a.orders_subtotal, a.orders_taxes, \
                a.orders_total, a.orders_paid, b.user_gov_id, b.user_id, \
                b.user_company, CONCAT(b.user_name,' ',b.user_last_name), \
                c.payment_date, c.payment_type, c.payment_status, \
                c.payment_txn_id, c.payment_total, d.shipping_address, \
                d.shipping_city, d.shipping_state, d.shipping_country, \
                d.shipping_cost \
                FROM orders AS a \
                INNER JOIN users AS b \
                ON a.user_id = b.user_id \
                INNER JOIN payment AS c \
                ON a.order_id = c.order_id \
                INNER JOIN shipping AS d \
                ON a.order_id = d.order_id \
                WHERE d.shipping_city = %s OR d.shipping_state = %s \
                OR d.shipping_country = %s"
        data = mysql_run(sql, (value, value, value))
        # FETCH RESULT
        for val in data:
            order = dict_order(val)
            results.append(order)
        return jsonify(results)
    except:
        return jsonify({"message": "Orders not found"}), 404


@app_views.route('/orders/user_id/', methods=['GET'],
                 strict_slashes=False)
def orders_by_user_id():
    try:
        results = []
        # VALID TOKEN
        token = request.headers.get('x-auth-token')
        if not valid_token(token):
            return jsonify({"message": "Unauthorized"}), 401
        user_id = getid_token(token)
        # QUERY
        sql = "SELECT a.order_id, a.orders_date, a.orders_subtotal, a.orders_taxes, \
                a.orders_total, a.orders_paid, b.user_gov_id, b.user_id, \
                b.user_company, CONCAT(b.user_name,' ',b.user_last_name), \
                c.payment_date, c.payment_type, c.payment_status, \
                c.payment_txn_id, c.payment_total, d.shipping_address, \
                d.shipping_city, d.shipping_state, d.shipping_country, \
                d.shipping_cost \
                FROM orders AS a \
                INNER JOIN users AS b \
                ON a.user_id = b.user_id \
                INNER JOIN payment AS c \
                ON a.order_id = c.order_id \
                INNER JOIN shipping AS d \
                ON a.order_id = d.order_id \
                WHERE a.user_id = %s"
        data = mysql_run(sql, (user_id, ))
        # FETCH RESULT
        for val in data:
            order = dict_order(val)
            results.append(order)
        return jsonify(results)
    except:
        return jsonify({"message": "Orders not found"}), 404


@app_views.route('/orders/search/', methods=['GET'],
                 strict_slashes=False)
def orders_by_filter():
    try:
        results = []
        # VALID TOKEN
        token = request.headers.get('x-auth-token')
        if not valid_token(token):
            return jsonify({"message": "Unauthorized"}), 401
        # PARAMS
        k_arg = request.args.keys()
        for karg in k_arg:
            if len(k_arg) != 2 or karg not in ["orderby", "search"]:
                return jsonify({"message": "Bad request"}), 400
        orderby = request.args.get('orderby')
        search = request.args.get('search')
        if orderby not in ["datedesc", "dateasc", "totaldesc", "totalasc",
                           "none"]:
            return jsonify({"message": "Bad request"}), 400
        # QUERY
        sql_orderby = {
            "datedesc": "ORDER BY a.orders_date DESC",
            "dateasc": "ORDER BY a.orders_date ASC",
            "totaldesc": "ORDER BY c.payment_total, a.orders_total DESC",
            "totalasc": "ORDER BY c.payment_total, a.orders_total ASC",
            "none": ""
        }
        sql_like = "%{}%".format(search)
        
        sql = "SELECT a.order_id, a.orders_date, a.orders_subtotal, a.orders_taxes, \
                a.orders_total, a.orders_paid, b.user_gov_id, b.user_id, \
                b.user_company, CONCAT(b.user_name,' ',b.user_last_name), \
                c.payment_date, c.payment_type, c.payment_status, \
                c.payment_txn_id, c.payment_total, d.shipping_address, \
                d.shipping_city, d.shipping_state, d.shipping_country, \
                d.shipping_cost \
                FROM orders AS a \
                INNER JOIN users AS b \
                ON a.user_id = b.user_id \
                INNER JOIN payment AS c \
                ON a.order_id = c.order_id \
                INNER JOIN shipping AS d \
                ON a.order_id = d.order_id \
                WHERE b.user_company LIKE %s OR d.shipping_city LIKE %s \
                OR d.shipping_state LIKE %s OR d.shipping_country LIKE %s \
                {} ".format(sql_orderby.get(orderby))
        data = mysql_run(sql, (sql_like, sql_like, sql_like, sql_like))
        # FETCH RESULT
        for val in data:
            order = dict_order(val)
            results.append(order)
        return jsonify(results)
    except:
        return jsonify({"message": "Orders not found"}), 404


@app_views.route('/orders/', methods=['POST'], strict_slashes=False)
def create_order():
    try:
        # VALID TOKEN
        token = request.headers.get('x-auth-token')
        if not valid_token(token):
            return jsonify({"message": "Unauthorized"}), 401
        args = request.get_json()
        # PARAMS
        k_arg = args.keys()
        for _k_arg in k_arg:
            if _k_arg not in ["orders_subtotal", "shipping_address",
                              "shipping_city", "shipping_state",
                              "shipping_country", "payment_type"]:
                return jsonify({"message": "Bad request"}), 400
        orders_subtotal = args.get("orders_subtotal")
        shipping_address = args.get("shipping_address")
        shipping_city = args.get("shipping_city")
        shipping_state = args.get("shipping_state")
        shipping_country = args.get("shipping_country")
        payment_type = args.get("payment_type")
        if payment_type not in ["cash", "credit card", "bank check"]:
            return jsonify({"message": "Bad request"}), 400
        orders_taxes = random.randrange(1, int(orders_subtotal / 2))
        orders_total = orders_taxes + orders_subtotal
        orders_paid = 0
        shipping_cost = random.randrange(50, 200)
        payment_txn_id = random.randrange(10000, 99999)
        payment_total = orders_total + shipping_cost
        payment_status = "ok"
        user_id = getid_token(token)
        # CREATE ORDER
        order_id = uuid.uuid4()
        sql = "INSERT INTO orders (order_id, orders_subtotal, orders_taxes, orders_total, \
            orders_paid, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
        mysql_run(sql, (order_id, orders_subtotal, orders_taxes, orders_total,
                        orders_paid, user_id), True)
        # CREATE SHIPPING
        shipping_id = uuid.uuid4()
        sql = "INSERT INTO shipping (shipping_id, shipping_address, shipping_city, \
            shipping_state, shipping_country, shipping_cost, order_id) \
            VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mysql_run(sql, (shipping_id, shipping_address, shipping_city,
                        shipping_state, shipping_country, shipping_cost,
                        order_id), True)
        # CREATE PAYMENT
        payment_id = uuid.uuid4()
        sql = "INSERT INTO payment (payment_id, payment_type, \
            payment_txn_id, payment_total, payment_status, order_id) \
            VALUES (%s, %s, %s, %s, %s, %s)"
        mysql_run(sql, (payment_id, payment_type, payment_txn_id,
                        payment_total, payment_status, order_id), True)
        mysql.connection.commit()
        # QUERY NEW ORDER
        sql = "SELECT a.order_id, a.orders_date, a.orders_subtotal, a.orders_taxes, \
            a.orders_total, a.orders_paid, b.user_gov_id, b.user_id, \
            b.user_company, CONCAT(b.user_name,' ',b.user_last_name), \
            c.payment_date, c.payment_type, c.payment_status, \
            c.payment_txn_id, c.payment_total, d.shipping_address, \
            d.shipping_city, d.shipping_state, d.shipping_country, \
            d.shipping_cost \
            FROM orders AS a \
            INNER JOIN users AS b \
            ON a.user_id = b.user_id \
            INNER JOIN payment AS c \
            ON a.order_id = c.order_id \
            INNER JOIN shipping AS d \
            ON a.order_id = d.order_id \
            WHERE a.order_id = %s"
        data = mysql_run(sql, (order_id,))
        # FETCH NEW  RESULT
        order = {}
        for val in data:
            order = dict_order(val)
        return jsonify(order)
    except:
        print(sys.exc_info())
        return jsonify({"message": "Error"}), 500
