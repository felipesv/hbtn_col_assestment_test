from flask import render_template, session, request, redirect
from . import routes
import requests


@routes.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        url = 'http://localhost:5000/api/v1/login'
        password = request.form["password"]
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            data_res = response.json()
            api_key = data_res.get('api_key')
            session['api_key'] = api_key
            return redirect('/orders')
        else:
            return render_template('login.html', message=response.json())
    return render_template('login.html')


@routes.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')
