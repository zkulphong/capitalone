from __future__ import division
from flask import Flask, render_template, request
import googlemaps
from datetime import datetime, time, date, timedelta
import pandas as pd
import csv
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index', methods=['GET'])
def returnIndex():
    return render_template("index.html")

@app.route('/visualize', methods=['GET'])
def visualize():
    return render_template("visualize.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    csv_name = "static/sfpd_dispatch_data_subset.csv"
    data = pd.read_csv(csv_name)
    date_format = "%Y-%m-%d %H:%M:%S.%f UTC"
    time_format = "%H:%M"
    top_ten_closest = []
    top_ten_indices = []

    default_address = 'Golden Gate Bridge, San Francisco, CA'
    default_time = "12:00"
    address = request.form.get('address', default_address)

    time = str(request.form.get('time', default_time))
    time_formated = datetime.strptime(time, time_format)
    time_only = datetime.time(time_formated)

    gmaps = googlemaps.Client(key='AIzaSyAzlAjqxxSm-CjZb3JMk4k3vQ8UUOgr3fk')
    geocode_result = gmaps.geocode(address)
    filtered_result_lat = float(geocode_result[0]['geometry']['location']['lat'])
    filtered_result_long = float(geocode_result[0]['geometry']['location']['lng'])

    time_indices_withinHour = []

    for index, row in data.iterrows():
        temp = datetime.time(datetime.strptime(data['received_timestamp'][index], date_format))
        time1 = datetime.combine(date.today(), temp)
        time2 = datetime.combine(date.today(), time_only)
        if (time1 - time2 < timedelta(hours=1) and time1 - time2 > timedelta(hours = 0)) or (time2 - time1 < timedelta(hours=1) and time2 - time1 > timedelta(hours = 0)):
            time_indices_withinHour.append(index)

    for index in time_indices_withinHour:
        row_lat = data['latitude'][index]
        row_long = data['longitude'][index]
        distance = math.sqrt(((filtered_result_lat - row_lat)**2)+((filtered_result_long - row_long)**2))
        top_ten_closest.append(distance)
        top_ten_indices.append(index)

    dTypes = {}
    for index in top_ten_indices:
        ref = top_ten_indices.index(index)
        if data["unit_type"][index] not in dTypes:
            dTypes[data["call_type"][index]] = (1/(top_ten_closest[ref]**2));
        else:
            dTypes[data["call_type"][index]] = dTypes[data["call_type"][index]] + (1/(top_ten_closest[ref]**2))

    dTypes = (sorted(dTypes.iteritems(), key=lambda (k,v): (v,k)))

    prediction = ''
    prediction_val = 0
    prob_denominator = 0
    for key, value in dTypes:
        prediction = key
        prediction_val = value
        prob_denominator = prob_denominator + value

    probability = str(int(round(prediction_val*100/prob_denominator)))

    return render_template("predict.html", prediction = "Most Likely Dispatch at " + address + " at " + time + " is " + prediction + " with " + probability + "% probability")

@app.route('/improve', methods=['GET'])
def improve():
    return render_template("improve.html")

if __name__ == '__main__':
    app.run(debug=True)
