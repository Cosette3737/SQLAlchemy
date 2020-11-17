# 1. import Flask
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite',  echo=True )

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Base.classes.keys()

measurement = Base.classes.measurement
Station = Base.classes.station




# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return(
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/add start date in YYY-MM-DD format<br/>" 
        f"/api/v1.0/<start>/<end> add start date and end date in YYY-MM-DD format")
        



# 4. Define what to do when a user hits the /about route


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).order_by(measurement.date.desc()).all()
    session.close()
    all_precipitation=list(np.ravel(results))
    return jsonify(all_precipitation)
   


@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    results=session.query(Station.name).all()
    session.close()
    all_stations=list(np.ravel(results))
    return jsonify(all_stations)
                                                                                      
  
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    lst_date=str(session.query(measurement.date).order_by(measurement.date.desc()).first())
    date_dt=dt.datetime.strptime(lst_date,"('%Y-%m-%d',)")
    query_date=date_dt-dt.timedelta(days=366)
    results=session.query(measurement.tobs, measurement.date).filter(measurement.station=="USC00519281").filter(measurement.date>query_date).all()
    session.close()
    all_tobs=list(np.ravel(results))
    return jsonify(all_tobs)
    
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    #query_date = dt.datetime.strptime(start,"('%Y-%m-%d',)")
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date>start).all()
    session.close()
    all_start=list(np.ravel(results))
    return jsonify(all_start)
  

@app.route("/api/v1.0/<start>/<end>")
def start_end(start_end):
    session = Session(engine)
    #lst_date=str(session.query(measurement.date).order_by(measurement.date.desc()).first())
    #date_dt=dt.datetime.strptime(lst_date,"('%Y-%m-%d',)")
    #query_date=date_dt-dt.timedelta(days=366)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date<end ).filter(measurement.date>start).all()
    session.close()
    all_start=list(np.ravel(results))
    return jsonify(all_start)

if __name__ == '__main__':
    app.run(debug=True)

