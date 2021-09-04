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
    f"<b>Available routes:</b></br>"
    f"/api/v1.0/precipitation</br>"
    f"/api/v1.0/stations</br>"
    f"/api/v1.0/tobs</br>"
    f"/api/v1.0/<b>< start ></b>  <i>(where <b>< start ></b> is of form YYYY-mm-dd)</i></br>"
    f"/api/v1.0/<b>< start ></b>/<b>< end ></b> <i>(where <b>< start ></b> and <b>< end ></b> are of form YYYY-mm-dd)</i>"
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
    '''Return a JSON list of stations from the dataset'''
    # Create our session (link) from Python to the DB, queries, close
    session = Session(engine)
    stationstuple = session.query(Station.name).all()
    session.close()
    stationslist = [station1[0] for station1 in stationstuple]
    return jsonify(stationslist)

## Return a JSON list of temperature obsevations
@app.route("/api/v1.0/tobs")
def tobs():
    '''Return JSON list of temperature observations for previous year of most active station'''
    # Create our session (link) from Python to the DB, queries, close
    session = Session(engine)
    recent_date = (session.query(Measurement.date)
                          .order_by(Measurement.date.desc())
                          .first()
                  )
    most_recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d")
    one_year_earlier = most_recent_date - dt.timedelta(weeks=52)
    active_stations = (session.query(Station.name, Station.station, func.count(Station.name))
                              .filter(Station.station == Measurement.station)
                              .group_by(Station.name)
                              .order_by(func.count(Station.name).desc())
                              .all()
                      )
    active_station = active_stations[0][1]
    tobstuple = (session.query(Measurement.date, Measurement.tobs)
                        .filter(Measurement.station == active_station)
                        .filter(Measurement.date >= one_year_earlier)
                        .all()
                )
    session.close()
    # tobs_dict = {}
    # for date1, tobs in tobstuple:
    #     tobs_dict[date1] = tobs
    tobs_list = [tobs[1] for tobs in tobstuple]
    return jsonify(tobs_list)

## Return a JSON list of the min, avg, and max temperature for
##  a given start-end date range.
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    session = Session(engine)
    end_date = end
    start_date = start
    tobstuple = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs))
                        .filter(Measurement.date >= start_date)
                        .filter(Measurement.date < end_date)
                        .first()
                )
    session.close()
    return (
        f"Start date: {start_date}.  End date: {end_date}.</br>"
        f"=================================</br>"
        f"Min temp {tobstuple[0]:.1f}</br>"
        f"Avg temp {tobstuple[1]:.1f}</br>"
        f"Max temp {tobstuple[2]:.1f}"
        )

## Return a JSON list of the min, avg, and max temperature for
##  a given start date range.
@app.route("/api/v1.0/<start>")
def startonly(start):
    session = Session(engine)
    recent_date = (session.query(Measurement.date)
                          .order_by(Measurement.date.desc())
                          .first()
                  )
    most_recent_date = dt.datetime.strptime(recent_date[0], "%Y-%m-%d")
    end_date = most_recent_date
    start_date = start
    tobstuple = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs))
                        .filter(Measurement.date >= start_date)
                        .filter(Measurement.date < end_date)
                        .first()
                )
    session.close()
    return (
        f"Start date: {start_date}.  End date: {end_date}.</br>"
        f"=================================</br>"
        f"Min temp {tobstuple[0]:.1f}</br>"
        f"Avg temp {tobstuple[1]:.1f}</br>"
        f"Max temp {tobstuple[2]:.1f}"
        )

# Run if invoked by python command line
if __name__ == "__main__":
    app.run(debug=True)