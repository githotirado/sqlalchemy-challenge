# Climate App API

# Python SQL toolkit and Object Relational Mapper, Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# additional helpful imports
import numpy as np
import datetime as dt

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Set up FLASK
app = Flask(__name__)

# Define the routes
## Home Page: list all routes that are available
@app.route("/")
def home():
    '''List all available api routes'''
    return (
    f"Available routes:</br>"
    f"/api/v1.0/precipitation</br>"
    f"/api/v1.0/stations</br>"
    f"/api/v1.0/tobs</br>"
    f"/api/v1.0/< start ></br>"
    f"/api/v1.0/< start >/< end >"
    )

## Precipitation: return JSON of query results dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    '''Return JSON of precipitation results dictionary'''
    # Create our session (link) from Python to the DB, queries, close
    session = Session(engine)
    recent_date = (session.query(Measurement.date)
                          .order_by(Measurement.date.desc())
                          .first()
                  )
    most_recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d")
    one_year_earlier = most_recent_date - dt.timedelta(weeks=52)
    date_precip = (session.query(Measurement.date, Measurement.prcp)
                          .filter(Measurement.date >= one_year_earlier)
                          .all()
                  )
    session.close()
    # Save results into a dictionary, return dictionary jsonified
    date_precip_dict = {}
    for date1, precip1 in date_precip:
        date_precip_dict[date1] = precip1

    return jsonify(date_precip_dict)

## Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    '''Return JSON list of statiions from the dataset'''
    # Create our session (link) from Python to the DB, queries, close
    session = Session(engine)
    stationstuple = session.query(Station.name).all()
    session.close()
    stationslist = [station1[0] for station1 in stationstuple]
    return jsonify(stationslist)

## Return a JSON list of temperature obsevations
@app.route("/api/v1.0/tobs")
def tobs():
    return "The tobs URL"

## Return a JSON list of the min, avg, and max temperature for
##  a given start or start-end date range.
# @app.route("/api/v1.0/<start>" "/app/v1.0/<start>/<end>")
@app.route("/api/v1.0/<start>/<end>")
def startdate(start, end):
    return "Start and start/end"

# Run if invoked by python command line
if __name__ == "__main__":
    app.run(debug=True)