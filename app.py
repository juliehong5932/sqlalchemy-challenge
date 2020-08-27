

#import Flask
from flask import Flask, jsonify
import numpy as np
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine,reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#Create app 
app = Flask(__name__)

#define routes

@app.route("/")
def welcome():
    return (
        f"Welcome to Climate App<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"

@app.route("/api/v1.0/precipitation")
def prcp():
    prcp = session.query(Measurement.date, Measurement.prcp ).\
        filter(Measurement.date > year_ago).\
        order_by(Measurement.date).all()
    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    lowest = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').all()
    highest = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').all()
    average = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').all()
    return jsonify(lowest, highest, average)

@app.route("/api/v1.0/<start_date>")
def start_date_data(start_date):
    start_date = [func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    start_date_data = session.query(start_date).\
        filter(Measurement.date >= start_date).all()
    return jsonify(start_date_data)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date_data(start_date, end_date):
    start_end_date = [func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    start_date_data = session.query(start_end_date).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    return jsonify(start_end_date_data)

if __name__ == "__main__":
    app.run(debug=True)