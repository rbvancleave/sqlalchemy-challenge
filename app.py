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

# Flask Setup
app = Flask(__name__)

# Flash Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and prcp"""
    # Query all dates
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    data = []
    for date,prcp in results:
        date_dict = {}
        date_dict['date']=date
        date_dict['prcp']=prcp
        data.append(date_dict)

    return jsonify(data)

@app.route("/api/v1.0/station")
def stations():
    session = Session(engine)

    results = session.query(Station.station)
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start)\
        .filter(Measurement.station=='USC00519281').all()
    
    data = []

    for date,tobs in results:
        date_dict = {}
        date_dict['date']=date
        date_dict['tobs']=tobs
        data.append(date_dict)

     return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)






