from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from metro import Station,Metro_Route

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'MetroService.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('db created')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB dropped')

@app.cli.command('db_seed')
def db_seed():
    user1 = Customer(
        id = 1,
        name = 'Film',
        user = 'filmpat',
        passwd = '1234',
        phone_num = '0891234567',
        user_type = 'Student'
    )
    db.session.add(user1)

    A1 = Stations(
        station_id = 1,
        name = 'A1',
        train_interval_time = 5,
        train_standby_time = 1,
        first_run_time = '05:46',
        last_run_time = '22:46'
    )

    A2 = Stations(
        station_id=2,
        name='A2',
        train_interval_time=5,
        train_standby_time=1,
        first_run_time='05:50',
        last_run_time='22:50'
    )

    A3 = Stations(
        station_id=3,
        name='A3',
        train_interval_time=5,
        train_standby_time=1,
        first_run_time='05:52',
        last_run_time='22:52'
    )

    A4 = Stations(
        station_id=4,
        name='A4',
        train_interval_time=5,
        train_standby_time=1,
        first_run_time='05:55',
        last_run_time='22:55'
    )

    A5 = Stations(
        station_id=5,
        name='A5',
        train_interval_time=5,
        train_standby_time=1,
        first_run_time='05:59',
        last_run_time='22:59'
    )

    B1 = Stations(
        station_id=6,
        name='B1',
        train_interval_time=5,
        train_standby_time=1,
        first_run_time='05:30',
        last_run_time='22:30'
    )

    B2 = Stations(
        station_id=7,
        name='B2',
        train_interval_time=5,
        train_standby_time=1,
        first_run_time='05:35',
        last_run_time='22:35'
    )

    B3 = Stations(
        station_id=8,
        name='B3',
        train_interval_time=5,
        train_standby_time=1,
        first_run_time='05:39',
        last_run_time='22:39'
    )

    B4 = Stations(
        station_id=9,
        name='B4',
        train_interval_time=5,
        train_standby_time=1,
        first_run_time='05:42',
        last_run_time='22:42'
    )

    station_list = [A1, A2, A3, A4, A5, B1, B2, B3, B4]
    for station in station_list:
        db.session.add(station)
        db.session.commit()

    print("Database seeded")

@app.route('/')
def welcome():
    return 'Hello, this is the Metro Service'

@app.route('/users')
def users():
    customer_list = Customer.query.all()
    result = customers_schema.dump(customer_list)
    return jsonify(result)

@app.route('/stations')
def stations():
    station_list = Stations.query.all()
    result = stations_schema.dump(station_list)
    return jsonify(result)

@app.route('/stations/<string:name>')
def describe_station(name:str):
    station_list = Stations.query.all()
    for station in station_list:
        if name in station.name:
            ThisStation = Station(name,station.first_run_time,station.last_run_time)
            return ThisStation.describe_station()
    return {"Error": "invalid station"}

@app.route('/get_arrival_time/<string:name>')
def get_arrival_time(name:str):
    station_list = Stations.query.all()
    for station in station_list:
        if name in station.name:
            ThisStation = Station(name,station.first_run_time,station.last_run_time)
    try:
        near_time = ThisStation.arrival_time(time='now')
        result = dict()
        if len(near_time) == 0:
            return jsonify(message = "Sorry, No trains are in service")
        for i in range(len(near_time)):
            result[i] = near_time[i][1]
        return result

    except:
        return {"Error": "invalid station"}


@app.route('/get_arrival_time/<string:name>/<string:time>')
def get_arrival_time_time(name:str,time:str):
    station_list = Stations.query.all()
    for station in station_list:
        if name in station.name:
            ThisStation = Station(name,station.first_run_time,station.last_run_time)

    try:
        near_time = ThisStation.arrival_time(time)
        result = dict()
        if len(near_time) == 0:
            return jsonify(message = "Sorry, No trains are in service")
        for i in range(len(near_time)):
            result[i] = near_time[i][1]
        return result

    except:
        return {"Error": "invalid station"}

@app.route('/get_route/<string:stationA>/<string:stationB>')
def get_route(stationA:str,stationB:str):
    metro_route = Metro_Route()

    station_list = Stations.query.all()
    for station in station_list:
        if stationA in station.name:
            stationA_obj = Station(stationA,station.first_run_time,station.last_run_time)
        if stationB in station.name:
            stationB_obj = Station(stationB,station.first_run_time,station.last_run_time)

    try:
        route,total_time,ticket_price = metro_route.get_route(stationA_obj,stationB_obj)
        result = dict()
        result['route'] = route
        result['total_time'] = total_time
        result['ticket_price'] = ticket_price
        return result
    except:
        return {"Error": "invalid station"}

@app.route('/get_destination_time/<string:stationA>/<string:stationB>')
def get_destination_time(stationA:str,stationB:str):
    metro_route = Metro_Route()

    station_list = Stations.query.all()
    for station in station_list:
        if stationA in station.name:
            stationA_obj = Station(stationA,station.first_run_time,station.last_run_time)
        if stationB in station.name:
            stationB_obj = Station(stationB,station.first_run_time,station.last_run_time)
    try:
        result = metro_route.get_destination_time(stationA_obj,stationB_obj,time='now')
        return result
    except:
        return {"Error": "invalid station"}

class Customer(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    user = Column(String)
    passwd = Column(String)
    phone_num = Column(String)
    user_type = Column(String)

class Stations(db.Model):
    __tablename__ = 'stations'
    station_id = Column(Integer,primary_key=True,unique=True)
    name = Column(String, unique=True)
    train_interval_time = Column(Float)
    train_standby_time = Column(Float)
    first_run_time = Column(String)
    last_run_time = Column(String)

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'user', 'user_type')

class StationsSchema(ma.Schema):
    class Meta:
        fields = ('station_id','name','first_run_time','last_run_time')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many = True)

station_schema = StationsSchema()
stations_schema = StationsSchema(many = True)

if __name__ == '__main__':
    app.run()

