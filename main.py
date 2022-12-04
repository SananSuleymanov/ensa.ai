from flask import Flask, request, url_for, redirect, render_template, flash, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
import numpy as np
import tensorflow as tf
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import login_user
import sign_up
import Data
import plot
from form import RegistrationForm

load_dotenv()

app = Flask(__name__)
app.secret_key= os.getenv('SECRET_KEY')
api = Api(app)
bcrypt = Bcrypt(app)

model = tf.keras.models.load_model('ensa.h5')


class load(Resource):

    def norm(self, array):
        mean = np.array([22.11236842, 428.59473684])
        vars = np.array([5.23060865e-02, 1.78432290e+03])
        stds = vars ** 0.5
        return (array-mean)/stds

    def get(self, uuid, co2, humidity, point_name):
        output =None
        raw_input = np.array([[humidity, co2]])
        input = self.norm(raw_input)
        value = model.predict(input)

        if value[0][0]>value[0][1] and value[0][0]>value[0][2]:
            output ='low'
        if value[0][1]>value[0][0] and value[0][1]>value[0][2]:
            output ='medium'
        if value[0][2]>value[0][0] and value[0][2]>value[0][1]:
            output ='high'
        low = str(round(value[0][0], 2))
        medium = str(round(value[0][1], 2))
        high = str(round(value[0][2],2))
        data = Data.sql()
        data.send(co2, humidity, output, low, medium, high, uuid, point_name)
        return jsonify({'Point name': point_name,
                        'Low probability': low,
                        'Medium probability': medium,
                        'High probability': high,
                        'CO2 value:': co2,
                        'Humidity value': humidity,
                        'load': output})

api.add_resource(load, '/load/<string:uuid>/<int:humidity>/<int:co2>/<string:point_name>')
@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        if request.form['bt_sign']=='SIGN UP':
            return redirect(url_for('signup'))
        elif request.form['bt_sign']=='LOGIN':
            return redirect(url_for('login'))

    return render_template('landing.html')

@app.route('/visualize_co2')
def visualize_co2():
    data = Data.sql()
    time, co2, hum = data.array()
    d = figure(time, co2, hum)
    image = d.plot_co2()
    return send_file(image, mimetype='img/png')


@app.route('/visualize_hum')
def visualize_hum():

    data = Data.sql()
    time, co2, hum = data.array()
    d = figure(time, co2, hum)
    image = d.plot_hum()
    return send_file(image, mimetype='img/png')


@app.route('/dashboard/<email>', methods= ['POST', 'GET'])
def dashboard(email):
    data = Data.sql()
    options = data.points_get(email)
    uuid= data.uuid(email)
    if request.method=='POST':
        try:
            co2_m, humidity, pred, val0, val1, val2 = data.get(request.form['modul_option'], email)
            time, co2, hum = data.array()
            hour_data = data.array()
            print('co2: ', co2_m)
        except:
            co2_m= humidity=pred=val0=val1=val2 = '--'
            time=co2= hum = '--'
            hour_data = [], [], []
            print('excepted1')
        p= plot.plot_graph(hour_data)
        graph= p.plot_data()

        
        if request.form['btn']=='Submit':
            selected=request.form['modul_option']
            return render_template('Dashboard.html',  co2 = co2_m, humidity = humidity, prediction= pred, val0 = val0,
                           val1 = val1, val2 = val2, max1 =1500, max2 = 50, values_co2 = co2, values_hum=hum, labels = time, options = options,
                           graph= graph, uuid=uuid, selected=selected)

        elif request.form['btn']=='ADD':
            data.point_add(request.form['pcn'])
            return render_template('Dashboard.html',  co2 = co2_m, humidity = humidity, prediction= pred, val0 = val0,
                           val1 = val1, val2 = val2, max1 =1500, max2 = 50, values_co2 = co2, values_hum=hum, labels = time, options = data.points_get(email),
                           graph=graph, uuid=uuid)

            
    else:
        try:
            co2_m, humidity, pred, val0, val1, val2 = data.get(options[0], email )
            time, co2, hum = data.array()
            hour_data = data.array()
        except:
            co2_m= humidity=pred=val0=val1=val2 = '--'
            time=co2= hum = '--'
            hour_data = [], [], []
            print('excepted2')

        p= plot.plot_graph(hour_data)
        graph= p.plot_data()

        
        return render_template('Dashboard.html',  co2 = co2_m, humidity = humidity, prediction= pred, val0 = val0,
                           val1 = val1, val2 = val2, max1 =1500, max2 = 50, values_co2 = co2, values_hum=hum, labels = time, options = options,
                           graph=graph, uuid=uuid)

'''
Login Page
'''
@app.route('/login', methods = ['POST', 'GET'])
def login():

    error = None
    if request.method == 'POST':
       
        lg = login_user.signin(request.form['nm'], request.form['pw'], bcrypt=bcrypt)
        status, _ = lg.login_us()
        if status is False:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
        else:

            flash('You were successfully logged in')
            return redirect(url_for('dashboard' , email = request.form['nm']))
    else:
        return render_template('login.html', error = error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error=None
    form= RegistrationForm()
    if request.method=='POST':
        sg=sign_up.signup(form.email.data, bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        if form.validate_on_submit():
            if sg.signup_us() is False:
                error='You already registered'
                return render_template('sign_up.html', error=error, form=form)
            else:
                return redirect(url_for('login', error='You were successfully signed up'))   
            
        else:
            return render_template('sign_up.html', form=form)
    else:
        return render_template('sign_up.html', form=form)

if __name__ =='__main__':
    app.run(debug=True)