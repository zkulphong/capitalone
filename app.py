from __future__ import division
from flask import Flask, render_template, request
import googlemaps
from datetime import datetime, time, date, timedelta
import pandas as pd
import csv
import math

app = Flask(__name__)

#routing for index.html
@app.route('/')
def index():
    return render_template("index.html")

#routing for index.html when first launching website
@app.route('/index')
def returnIndex():
    return render_template("index.html")

#routing for visualize.html
@app.route('/visualize')
def visualize():
    return render_template("visualize.html")

#routing for predict.html
@app.route('/predict', methods=['POST', 'GET'])
def predict():

    #create dataframe
    csv_name = "static/sfpd_dispatch_data_subset.csv"
    data = pd.read_csv(csv_name)

    #set time formattings
    date_format = "%Y-%m-%d %H:%M:%S.%f UTC"
    time_format = "%H:%M"

    #store data within relevant time frame to 'received_timestamp'
    #algorithm originally took specific number of closest coordinates, hence the variable name
    top_closest = []

    #set default values
    default_address = 'Golden Gate Bridge, San Francisco, CA'
    default_time = "12:00"

    #get form responses and format results
    address = request.form.get('address', default_address)
    time = str(request.form.get('time', default_time))
    time_formated = datetime.strptime(time, time_format)
    time_only = datetime.time(time_formated)

    #get latitude and longitude from Google Maps Javascript API
    gmaps = googlemaps.Client(key='AIzaSyAzlAjqxxSm-CjZb3JMk4k3vQ8UUOgr3fk')
    geocode_result = gmaps.geocode(address)
    filtered_result_lat = float(geocode_result[0]['geometry']['location']['lat'])
    filtered_result_long = float(geocode_result[0]['geometry']['location']['lng'])

    #store indices with relevant time frame to 'received_timestamp'
    time_indices_withinHour = []

    #iterrate over dataframe to get relevant indices with 'received_timestamp' within 1 hour on either side of input 'time'
    for index, row in data.iterrows():
        temp = datetime.time(datetime.strptime(data['received_timestamp'][index], date_format))
        time1 = datetime.combine(date.today(), temp)
        time2 = datetime.combine(date.today(), time_only)
        if (time1 - time2 < timedelta(hours=1) and time1 - time2 > timedelta(hours = 0)) or (time2 - time1 < timedelta(hours=1) and time2 - time1 > timedelta(hours = 0)):
            time_indices_withinHour.append(index)

    #add distances from input 'address' to top_closest and indices in the dataframe to top_indices
    for index in time_indices_withinHour:
        row_lat = data['latitude'][index]
        row_long = data['longitude'][index]
        distance = math.sqrt(((filtered_result_lat - row_lat)**2)+((filtered_result_long - row_long)**2))
        top_closest.append(distance)

    #dictionary of keys of types of "unit_type" dispatches and values of weightings for each type
    #weighting calculated as sum of inverse square of distance within each "unit_type"
    dTypes = {}

    for index in time_indices_withinHour:
        ref = time_indices_withinHour.index(index)
        if data["unit_type"][index] not in dTypes:
            dTypes[data["unit_type"][index]] = (1/(top_closest[ref]**2));
        else:
            dTypes[data["unit_type"][index]] = dTypes[data["unit_type"][index]] + (1/(top_closest[ref]**2))

    dTypes = (sorted(dTypes.items(), key=lambda (k,v): (v,k)))

    #generate prediction and probability of prediction
    prediction = ''
    prediction_val = 0
    prob_denominator = 0
    for key, value in dTypes:
        prediction = key
        prediction_val = value
        prob_denominator = prob_denominator + value
    probability = str(int(round(prediction_val*100/prob_denominator)))

    return render_template("predict.html", prediction = "Most Likely Dispatch at " + address + " at " + time + " is " + prediction + " with " + probability + "% probability")

#routing improve.html
@app.route('/improve')
def improve():
    return render_template("improve.html")

if __name__ == '__main__':
    app.run(debug=True)
