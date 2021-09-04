# Climate App API
from flask import Flask, jsonify

app = Flask(__name__)

# Define the routes
## Home Page: list all routes that are available
@app.route("/")
def home():
    return '''
    Available routes:</br>
    /api/v1.0/precipitation</br>
    /api/v1.0/stations</br>
    /api/v1.0/tobs</br>
    /api/v1.0/<start></br>
    /api/v1.0/<start>/<end>
    '''

## Precipitation: return JSON of query results dictionary
@app.route("/api/v1.0/precipitation")

## Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")

## Return a JSON list of temperature obsevations
@app.route("/api/v1.0/tobs")

## Return a JSON lisst of the min, avg, and max temperature for
##  a given start or start-end date range.
# @app.route("/api/v1.0/<start>" "/app/v1.0/<start>/<end>")
@app.route("/app/v1.0/<start>/<end>")
def startdate(startdate, enddate):
    return "Start and start/end"

# Run if invoked by python command line
if __name__ == "__main__":
    app.run(debug=True)