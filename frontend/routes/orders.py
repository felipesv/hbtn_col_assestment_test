from flask import render_template, redirect, session, request
from . import routes
import requests


@routes.route('/orders', methods=['GET', 'POST'])
def index():
    if 'api_key' in session.keys():
        if request.method == 'POST':
            search = request.form['search']
            orderby = request.form['orderby']
            type = request.form['de_asc']
            orderby = "{}{}".format(orderby, type)
            url = "http://localhost:5000/api/v1/orders/search?orderby={}&search={}"
            url = url.format(orderby, search)
            headers = {'x-auth-token': session['api_key']}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                orders = response.json()
                print(orders)
                return render_template('orders.html', orders=orders)
            else:
                return render_template('orders.html', message=response.json())
        return render_template('orders.html')
    return redirect('/')
