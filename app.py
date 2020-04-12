
import numpy as np
from datetime import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create an engine for the chinook.sqlite database
engine = create_engine('sqlite:///Resources/hawaii.sqlite', echo=True, connect_args={"check_same_thread": False})
connect_args={"check_same_thread": False}
# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
#Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement
# Create a database session object
session = Session(engine)

# Flask Setup
app = Flask(__name__)

    
# Flask Routes
@app.route("/")
def welcome():
   
    return (
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/<end><br/>"          
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    maxdate=session.query(func.max(Measurement.date )).scalar()
    maxdate=dt.strptime(maxdate, '%Y-%m-%d')
    cutofdate = maxdate.replace(maxdate.year - 1).strftime('%Y-%m-%d')
    # Perform a query to retrieve the data and precipitation scores
    prec_data=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>cutofdate).order_by(Measurement.date.desc()).all()
    prec_data_list = dict(prec_data)
    return jsonify(prec_data_list)
    
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station, Station.name).all()
    station_list = list(stations)
    return jsonify(station_list)
@app.route("/api/v1.0/tobs")
def tobs():
    maxdate=session.query(func.max(Measurement.date )).scalar()
    maxdate=dt.strptime(maxdate, '%Y-%m-%d')
    cutofdate = maxdate.replace(maxdate.year - 1).strftime('%Y-%m-%d')
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>cutofdate).order_by(Measurement.date.desc()).all()
    tobs_data_list = list(tobs_data)
    return jsonify(tobs_data_list)
 
@app.route("/api/v1.0/<start>")
def start_date(start): 
     max_min_avg = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
     max_min_avg=list(max_min_avg)
     return jsonify(max_min_avg)
     
@app.route("/api/v1.0/<start>/<end>")
def start_end_date_(start,end): 
     max_min_avg = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date < end).all()
     max_min_avg=list(max_min_avg)
     return jsonify(max_min_avg)
         
    
# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)