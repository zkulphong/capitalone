import pandas as pd
import csv

csv_name = "sfpd-dispatch/sfpd_dispatch_data_subset.csv"
data = pd.read_csv(csv_name)

dTypes = {}
for dispatch in data["call_type_group"].values:
    if dispatch not in dTypes:
        dTypes[dispatch] = 0;
    else:
        dTypes[dispatch] = dTypes[dispatch] + 1

dTypes = (sorted(dTypes.iteritems(), key=lambda (k,v): (v,k), reverse=True))
print dTypes
