from flask import Flask,request, url_for, redirect, render_template,session
#from flask.ext.session import Session

from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_login import LoginManager
import MySQLdb
import pickle
import numpy as np
import os
import re

#TEMPLATE_DIR = os.path.abspath('C:/Users/DELL/PycharmProjects/Real_DeepLearning/venv/EDI/templates')
#STATIC_DIR = os.path.abspath('C:/Users/DELL/PycharmProjects/Real_DeepLearning/venv/EDI/static')
#TEMPLATE_DIR = os.path.abspath('G:/Pure Website Course/EDI/templates')
#STATIC_DIR = os.path.abspath('G:/Pure Website Course/EDI/static')

#app = Flask(__name__,template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app = Flask(__name__)
#from flask.ext.session import Session

SESSION_TYPE = 'memcache'

#sess = Session()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/diseases'
db=SQLAlchemy(app)



class Symptom(db.Model):
    __tablename__ = 'symptom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Integer,  nullable=False)

class Diseases(db.Model):
    __tablename__ = 'disease_name'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Account(db.Model):
    __tablename__ = 'account'
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email=db.Column(db.String(100),nullable=False)

    def __init__(self, username=None, password=None,email=None):
        self.username = username
        self.password = password
        self.email=email

model=pickle.load(open('model/model.pkl','rb'))


@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/login',methods=['POST','GET'])
def login():
    render_template('login.html')
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))
        #account = cursor.fetchone()
        account=Account.query.filter_by(username=username).first()
        print(account)
        if account :
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        details=Account( username,password,email)
        account = Account.query.filter_by(username=username).first()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            db.session.add(details)
            db.session.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/aboutUs")
def aboutUs():
    return render_template('aboutUs.html')

@app.route("/allDiseases")
def allDiseases():
    dise = Diseases.query.order_by(Diseases.name).all()
    return render_template('allDiseases.html',diseases=dise)

@app.route("/predict")
def predict():
    syms = Symptom.query.order_by(Symptom.name).all()
    return render_template('predict.html',syms=syms)


@app.route('/predict1',methods=['POST','GET'])
def predict1():
    int_features=[x for x in request.form.values()]
    print(int_features)
    l=[0]*132
    print(l)
    for i in range(len(int_features)):
        query= Symptom.query.filter_by(name=int_features[i]).first()
        l[query.id-1]=1
    print(l)

    prediction=model.predict([l])
    print(prediction)
    return render_template('predict.html',pred='Your Diseases is {}'.format(prediction[0]))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #sess.init_app(app)
    app.run(debug=True)