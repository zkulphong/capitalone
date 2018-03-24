import pandas as pd
import csv

#import dataset into dataframe
csv_name = "sfpd-dispatch/sfpd_dispatch_data_subset.csv"
data = pd.read_csv(csv_name)

#get dictionary with keys of types from "unit_type" and values counting the frequency of each type in dataset
dTypes = {}
for dispatch in data["unit_type"].values:
    if dispatch not in dTypes:
        dTypes[dispatch] = 1;
    else:
        dTypes[dispatch] = dTypes[dispatch] + 1

#sort dictionary by largest to smallest values
dTypes = (sorted(dTypes.iteritems(), key=lambda (k,v): (v,k), reverse=True))
print dTypes
