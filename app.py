from flask import Flask,request, url_for, redirect, render_template,session
from flask_sqlalchemy import SQLAlchemy
#from flask_googlemaps import GoogleMaps
#from flask_googlemaps import Map
import pickle
import numpy as np
import os
import re



app = Flask(__name__)
#GoogleMaps(app, key="8JZ7i18MjFuM35dJHq70n3Hx4")

SESSION_TYPE = 'memcache'



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/diseases'
db=SQLAlchemy(app)


loginid=[]

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
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email=db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(255), nullable=False)
    contact=db.Column(db.String(10),nullable=False)
    state = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(10), nullable=False)

class Doctor(db.Model):
    __tablename__ = 'docter'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    contact= db.Column(db.String(10), nullable=False)
    disease=db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(10), nullable=False)

def __init__(self, fullname=None, username=None, password=None,email=None,contact_no=None,state=None,city=None):
    self.fullname = fullname
    self.username = username
    self.password = password
    self.email=email
    self.contact=contact
    self.state=state
    self.city=city

def __init__(self, fullname=None, username=None, password=None,email=None,contact=None,disease=None,state=None,city=None):
    self.fullname = fullname
    self.username = username
    self.password = password
    self.email=email
    self.contact=contact
    self.disease=disease
    self.state=state
    self.city=city

model=pickle.load(open('model/model.pkl','rb'))


@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/loginpage',methods=['POST','GET'])
def loginpage():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))
        #account = cursor.fetchone()
        account = Account.query.filter_by(username=username).first()
        doctor = Doctor.query.filter_by(username=username).first()
        print(account)
        if account:
            loginid.append(username)
            loginid.append(0)
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        elif doctor:
            loginid.append(username)
            loginid.append(1)
            session['loggedin'] = True
            session['id'] = doctor.id
            session['username'] = doctor.username
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

@app.route('/registerdoc')
def registerdoc():
    return render_template('registerdoc.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'disease' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        disease =request.form['disease']
        state = request.form['state']
        city = request.form['city']

        details = Doctor(fullname = request.form['fullname'], username=request.form['username'], email=request.form['email'], password=request.form['password'], contact=request.form['contact'],disease=request.form['disease'], state=request.form['state'], city=request.form['city'])
        account = Doctor.query.filter_by(username=username).first()

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
            return render_template('login.html', msg=msg)

    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact= request.form['contact']
        state = request.form['state']
        city = request.form['city']

        details=Account(fullname=request.form['fullname'], username=request.form['username'], email=request.form['email'], password=request.form['password'], contact=request.form['contact'], state=request.form['state'], city=request.form['city'])
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
            return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/aboutUs")
def aboutUs():
    return render_template('aboutUs.html')

@app.route("/myaccount")
def myaccount():
    type=""
    if loginid[1]==0:
        type="User"
        account = Account.query.filter_by(username=loginid[0]).first()
    else:
        type = "Doctor"
        account = Doctor.query.filter_by(username=loginid[0]).first()
    return render_template('myaccount.html',account=account,type=type)

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
    account = Account.query.filter_by(username=loginid[0]).first()
    print(account.city)
    #list1 = Doctor.query.filter_by(disease=prediction[0] ).all()
    list = Doctor.query.filter(Doctor.disease.like(prediction[0]),Doctor.city.like(account.city))
    print(list)
    print(prediction)
    return render_template('result.html',result=format(prediction[0]),int_features=int_features,list=list)

@app.route("/map")
def map():
    # creating a map in the view
    '''mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ]
    )'''
    #return render_template('map.html', mymap=mymap, sndmap=sndmap)
    return render_template('map.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #sess.init_app(app)
    app.run(debug=True)