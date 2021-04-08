from flask import Flask,request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import MySQLdb
import pickle
import numpy as np
import os

TEMPLATE_DIR = os.path.abspath('C:/Users/DELL/PycharmProjects/Real_DeepLearning/venv/EDI/templates')
STATIC_DIR = os.path.abspath('C:/Users/DELL/PycharmProjects/Real_DeepLearning/venv/EDI/static')
#TEMPLATE_DIR = os.path.abspath('G:/Pure Website Course/EDI/templates')
#STATIC_DIR = os.path.abspath('G:/Pure Website Course/EDI/static')

app = Flask(__name__,template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/diseases'
db=SQLAlchemy(app)

class Symptom(db.Model):
    __tablename__ = 'symptom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Integer,  nullable=False)


model=pickle.load(open('G:/Third year/SEM2/EDI_6/Disease-Prediction-from-Symptoms-master/saved_model/model.pkl','rb'))


@app.route('/')
def hello_world():
    return render_template('index.html')


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
    #output='{0:.{1}f}'.format(prediction[0][1], 2)

if __name__ == '__main__':
    app.run(debug=True)