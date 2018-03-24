# Capital One Software Engineering Summit Summer Application 2018
# San Fransisco Emergency Dispatch Challenge
This web app was built for the Capital One Software Engineering Summer Application 2018 by Zak Kulphongpatana. The challenge required that Data Visuals, Predictions, and Optimizations regarding Emergency Calls in the San Francisco Area be displayed in a web application or webpage. The web app uses the Flask python and is hosted on Heroku(pulled from Github).

# Structure of Repository
The top level of the repository has 5 files and 3 folders. requirements.txt, runtime.txt, and Procfile indicate the Python libraries/versions required for the app, the version of Python, and the setup of the Flask App, respectively, for Heroku. App.py initializes the Flask application and generates the webpages. README.md is also included in the toplevel.
The three folders are analysisScripts_sfpd, static, and templates. analysisScripts_sfpd contains scripts used to analyze the dataset provided. Static contains the css, javascript, images, and dataset. Templates contains the html files. All Python is version 2.7.13.

# App.py
App.py initializes the Flask application and generates the webpages when the user navigates to the website. The index.html, visualize.html, and improve.html are rendered as the template without any changes by app.py. predict.html is rendered with the calculation of the dispatch prediction given an address and time. 

# predict.html Calculation
In order to calculate the most likely dispatch given an address and time, the sfpd_dispatch_data_subset.csv is first searched to find all dispatches received within one hour on either side of the inputed time creating a subset. Then all dispatches in this subset have their distance calculated from the inputed address using Google Maps API. For all unit_types found in this subset, a weighting is calculated for each unit_type. These weightings are calculated by summing the inverse square of distances(1/d^2) for all dispatches in the subset for each unit_type, so as to give greater weighting to dispatches closer to the address. The highest weighting indicates the most probable. The probability is calculated by dividing the weighting of the most likely unit_type by the sum of all unit_type weightings.

# Scripts in analysisScripts_sfpd folder
analysisScripts_sfpd contains the scripts I used to analyze the contents of the sfpd_dispatch_data_subset.csv which is contained within .../analysisScripts_sfpd/sfpd-dispatch
## callTypes.py, dispatchTypes.py, and unitTypes.py
callTypes.py, dispatchTypes.py, and unitType.py were used respectively to generate the values in the chartjs charts on the Visualize.html page. The scripts counted the amounts for the different subcategories of "call_type_group", "call_type", and "unit_type" respectively. An example of running a script from terminal is below:

```python callTypes.py```

### Outputs of callTypes.py
```
[('Potentially Life-Threatening', 4752), ('Non Life-threatening', 2468), ('Alarm', 2384), ('Fire', 392), (nan, 4)]
```
### Outputs of dispatchTypes.py
```
[('Medical Incident', 6791), ('Alarms', 1061), ('Structure Fire', 1029), ('Traffic Collision', 410), ('Outside Fire', 144), ('Other', 129), ('Citizen Assist / Service Call', 114), ('Gas Leak (Natural and LP Gases)', 86), ('Train / Rail Incident', 55), ('Water Rescue', 54), ('Vehicle Fire', 45), ('Elevator / Escalator Rescue', 23), ('Electrical Hazard', 21), ('Smoke Investigation (Outside)', 15), ('Odor (Strange / Unknown)', 10), ('Fuel Spill', 10), ('HazMat', 3)]
```
### Outputs of unitTypes.py
```
[('ENGINE', 3589), ('MEDIC', 3066), ('PRIVATE', 1154), ('TRUCK', 981), ('CHIEF', 726), ('RESCUE CAPTAIN', 272), ('RESCUE SQUAD', 168), ('SUPPORT', 33), ('INVESTIGATION', 11)]
```

## generateHeatMapNodes.py
generateHeatMapNodes.py was used to convert the coordinates of each dispatch into the javascript format required for Google Maps Heatmaps Javascript API. Result is printed to terminal to be copied and pasted into javascript file. As an improvement, I would implement my application such that generateHeatMapNodes.py wrote to a dynamic javascript file.

## longestDispatchTimes.py
longestDispatchTimes.py contains the calculations performed for the Analysis section of the Improve.html page. The average wait time for each zipcode was calculated. Wait time was calculated as the difference between the on_scene timestamp and received timestamp. Some dispatches did not have an on_scene timestamp so those dispatches were filtered out. The number of Dispatches within the time frame to each zipcode was calculated as well. Averages and Standard Deviations were printed out at the end.
### Ouputs of longestDispatchTimes.py
```
Zip Code, Average Wait Time, Number of Dispatches
94127 0:45:19.506329 79
94105 0:19:01.409909 222
94129 0:15:33.517241 29
94134 0:12:42.049751 201
94111 0:11:17.212903 155
94130 0:11:07.200000 35
94124 0:10:31.854117 425
94132 0:10:22.184971 173
94116 0:10:00.656976 172
94112 0:09:55.578947 361
94107 0:09:53.798701 308
94131 0:09:49.502923 171
94121 0:09:34 182
94133 0:09:29.472491 309
94158 0:09:25.644736 76
94108 0:09:22.722513 191
94104 0:09:19.517241 58
94103 0:09:16.409706 886
94123 0:09:10.916666 144
94122 0:09:07.193308 269
94102 0:09:05.541705 1067
94110 0:08:55.454948 677
94115 0:08:34.781818 385
94109 0:08:30.846381 677
94118 0:08:28.611607 224
94114 0:08:25.928802 309
94117 0:08:17.980000 300
Average of Average Wait Times
0:11:30.351655
Standard Deviation of Wait Times
7.01081799742minutes
Average of Average Wait Times without 94127
0:10:12.307244
Average Number of Dispatches
299
Standard Deviation of Number of Dispatches
249.957082736
```
# Areas of Improvement
#### Use analysisScripts_sfpd scripts outputs to dynamically update javascript files rather than manually entering ChartJS and Google Maps Javascript API data points. Allows, for changes to the dataset and automatically updating website accordingly.
#### Optimize speed of Flask application: predict.html loads slowly and requires page refresh
#### Fully implement Flat UI design
#### First time loading page is slow
# Resources Used
## Languages
### Python 2.7.13
### HTML5
### CSS3
### Javascript
## Python Libraries
### Werkzeug==0.14.1
### Jinja2==2.10
### MarkupSafe==1.0
### itsdangerous==0.24
### gunicorn==19.3.0
### Flask==0.12.2
### googlemaps==2.5.1
### numpy==1.13.3
### pandas==0.18.1
### pandas-datareader==0.5.0
### requests==2.18.4
## Javascript Resources
### Chartjs
### Google Maps Javascript API
## Hosting
### Heroku
