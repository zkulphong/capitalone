import pandas as pd
import csv

#import dataset into dataframe
csv_name = "sfpd-dispatch/sfpd_dispatch_data_subset.csv"
data = pd.read_csv(csv_name)

#get list of formatted heapmap coordinates
heatmapNodes = []
for node in data["location"].values:
        temp = "new google.maps.LatLng" + node
        heatmapNodes.append(temp)

#print Javascript for Google Maps Javascript API
for index in range(0,len(heatmapNodes)):
    if index == len(heatmapNodes) - 1:
        print heatmapNodes[index]
    else:
        print heatmapNodes[index] + ","
