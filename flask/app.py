from flask import Flask
from metro import Customer,Station,Metro_Route
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'MetroService.db')
db = SQLAlchemy(app)

@app.cli.command('db created')
def db_create():
    db.create_all()
    print('db created')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB dropped')

@app.route('/')
def welcome():
    return 'Hello, this is the Metro Service'

class Customer(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    user = Column(String)
    passwd = Column(String)
    phone_num = Column(String)
    user_type = Column(String)

class Station(db.Model):
    __tablename__ = 'stations'
    station_id = Column(Integer,primary_key=True,unique=True)
    name = Column(String, unique=True)
    train_interval_time = Column(Float)
    train_standby_time = Column(Float)
    first_run_time = Column(String)
    last_run_time = Column(String)

if __name__ == '__main__':
    app.run()

