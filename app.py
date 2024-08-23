
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()
Base.prepare(engine)


Measurment = Base.classes.measurement
Station = Base.classes.station



session = Session(engine)
app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii CLimate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
        )
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurment.date, Measurment.prcp).\
        filter(Measurment.date >= prev_year).all()
    
    session.close()
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()

    station = list(np.ravel(results))

    return jsonify(station=stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.tiemdelta(days=365)

    results =session.query(Measurment.tobs).\
    filter(Measurment.station == 'USC00519281').\
    filter(Measurment.date>= prev_year).all()

    session.close()
    
    print()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

@app.route("/api/v.1.0/temp/<start>")
@app.route("/api/v.1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    sel = [func.min(Measurment.tobs), func.avg(Measurment.tobs), func.max(Measurment.tobs)]

    if not end:
        start = st.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
        filter(Measurment.date >= start).all()

        session.close

        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    start = dt.datetime.strptime(start,"%m%d%Y")
    end = dt.datetime.strptime(end, "%M%d%Y")

    results = session.query(*sel).\
        filter(Measurment.date >= start).\
        filter(Measurment.date <= end).all()
    print(start)
    print(end)
    print(results)

    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)
        
if __name__ == "__main__":
    app.run(debug=True)
