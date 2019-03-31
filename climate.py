import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'start date'              (Enter start date in format YYYY-MM-DD) <br/> "
        f"/api/v1.0/'start date'/'end date'   (Enter start and date date in format YYYY-MM-DD) <br/>"
    )

    )


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation")
def precip():
    """Return a list of all precip amounts"""
    # Query all pecipitation amount
    
    try:
        results = session.query(Measurement.prcp).all()
        print(results)


    # Create a dictionary from the row data and append to a list of all_precip
        all_precip = []

        for precip in results:
            precip_dict = {}
            precip_dict["date"] = precip[0]
            precip_dict["prcp"] = precip[1]
            all_precip.append(precip_dict)
        session.commit()
        return jsonify(all_precip)

    except Exception:
            print("Error")
            session.rollback()

    return jsonify(all_precip)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of last 12 months of temperatures"""
    try: 
        current_time = dt.date.today()
        date = session.query(measurement.date, measurement.tobs).\
            order_by(measurement.date.desc()).first()

        year_ago = dt.datetime.strptime(date[0], "%Y-%m-%d") - dt.timedelta(days=366)

        sel=[measurement.date, measurement.tobs]
        # Query all stations
        results = session.query(*sel).filter(measurement.date >= year_ago).all()
        
        all_tobs = []
        for tobs_in in results:
            tobs_dict = {}
            tobs_dict["date"] = tobs_in[0]
            tobs_dict["tobs"] = tobs_in[1]
            all_tobs.append(tobs_dict)
        session.commit()
    except Exception:
        print("Error")
        session.rollback()

    return jsonify(all_tobs)

 if __name__ == '__main__':
     app.run(debug=True)
