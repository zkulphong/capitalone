import pandas as pd
import csv

csv_name = "sfpd-dispatch/sfpd_dispatch_data_subset.csv"
data = pd.read_csv(csv_name)

heatmapNodes = []
for node in data["location"].values:
        temp = "new google.maps.LatLng" + node
        heatmapNodes.append(temp)

for value in heatmapNodes:
    print value + ","
