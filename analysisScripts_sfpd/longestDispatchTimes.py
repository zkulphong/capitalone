import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import csv

#import dataset into dataframe
csv_name = "sfpd-dispatch/sfpd_dispatch_data_subset.csv"
data = pd.read_csv(csv_name)


date_format = "%Y-%m-%d %H:%M:%S.%f UTC"
dTypes = {}
zipcodeData = {}

for index, row in data.iterrows():
    if type(data["on_scene_timestamp"][index]) is str:
        if data["zipcode_of_incident"][index] not in dTypes:
            dTypes[data["zipcode_of_incident"][index]] = [datetime.strptime(data["on_scene_timestamp"][index], date_format) - datetime.strptime(data["received_timestamp"][index], date_format), 1]
        else:
            dTypes[data["zipcode_of_incident"][index]] = [dTypes[data["zipcode_of_incident"][index]][0] + datetime.strptime(data["on_scene_timestamp"][index], date_format) - datetime.strptime(data["received_timestamp"][index], date_format), dTypes[data["zipcode_of_incident"][index]][1] + 1]

for key, value in dTypes.iteritems():
    avg_time = value[0]/value[1]
    zipcodeData[key] = (avg_time, value[1])

zipcodeData = (sorted(zipcodeData.iteritems(), key=lambda (k,v): (v,k), reverse=True))

sumAvgTimes = timedelta(hours = 0)
sumNumIncidents = 0
std_deviationAvgWaitTime = []
std_deviationAvgNumInc = []

#print out Zip Codes, Average Wait Times, and Number of Dispatches
print "Zip Code, Average Wait Time, Number of Dispatches"
for index in range(0, len(zipcodeData)):
    print zipcodeData[index][0], zipcodeData[index][1][0], zipcodeData[index][1][1]
    sumAvgTimes = sumAvgTimes + zipcodeData[index][1][0]
    std_deviationAvgWaitTime.append(timedelta.total_seconds(zipcodeData[index][1][0]))
    sumNumIncidents = sumNumIncidents + zipcodeData[index][1][1]
    std_deviationAvgNumInc.append(zipcodeData[index][1][1])

#print out results
print "Average of Average Wait Times"
print str(sumAvgTimes/len(zipcodeData))
print "Standard Deviation of Wait Times"
print str(np.std(std_deviationAvgWaitTime)/60) + " minutes"
print "Average of Average Wait Times without 94127"
print str((sumAvgTimes - timedelta(minutes = 45, seconds = 19.506329))/(len(zipcodeData) - 1))
print "Average Number of Dispatches"
print str(sumNumIncidents/len(zipcodeData))
print "Standard Deviation of Number of Dispatches"
print np.std(std_deviationAvgNumInc)
