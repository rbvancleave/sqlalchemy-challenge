# Import Dependencies
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flash Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return a list of all dates and prcp"""
    # Query all dates
    results = session.query(Measurement.date,Measurement.prcp).all()

    data = []
    for date,prcp in results:
        date_dict = {}
        date_dict['date']=date
        date_dict['prcp']=prcp
        data.append(date_dict)

    return jsonify(data=data)

@app.route("/api/v1.0/station")
def stations():

    stations = session.query(Station.station).all()
    stations = list(np.ravel(stations))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    end = dt.date(2017,8,23)

    # Calculate the date one year from the last date in data set.
    for i in range(1,30):
        if end - dt.date(2016,8,i) == dt.timedelta(365):
            start = dt.date(2016,8,i)
            break
        else:
            continue

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start)\
        .filter(Measurement.station=='USC00519281').all()
    tobs = list(np.ravel(tobs))

    return jsonify(tobs = tobs)

if __name__ == '__main__':
    app.run(debug=True)






