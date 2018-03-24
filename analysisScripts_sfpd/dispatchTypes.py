import pandas as pd
import csv

#import dataset into dataframe
csv_name = "sfpd-dispatch/sfpd_dispatch_data_subset.csv"
data = pd.read_csv(csv_name)

dTypes = {}
for dispatch in data["call_type"].values:
    if dispatch not in dTypes:
        dTypes[dispatch] = 1;
    else:
        dTypes[dispatch] = dTypes[dispatch] + 1

dTypes = (sorted(dTypes.iteritems(), key=lambda (k,v): (v,k), reverse=True))
print dTypes
