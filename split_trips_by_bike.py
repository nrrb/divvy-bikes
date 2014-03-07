from __future__ import print_function
import csv
from datetime import datetime
import json
from math import ceil
import os

PATH = './trips_by_bike/'

def date(date_string):
    return datetime.strptime(date_string, '%m/%d/%Y %H:%M')

def number(int_string):
    return int(int_string.replace(',', ''))

def trip_cost(trip):
    if trip['usertype']=='Subscriber':
        cost = 0
        if trip['tripduration'] > 30*60:
            # 30-60 minutes: $1.50
            cost += 1.5
        if trip['tripduration'] > 60*60:
            # 60-90 minutes: +$3.00
            cost += 3.0
        if trip['tripduration'] > 90*60:
            # Each additional 30 minutes past 90 minutes: $6.00         
            addl_duration = trip['tripduration'] - 90*60
            cost += 6.0*ceil(addl_duration/(30.0*60))
        return cost
    else:
        cost = 0
        if trip['tripduration'] > 30*60:
            # 30-60 minutes: $2.00
            cost += 2.0
        if trip['tripduration'] > 60*60:
            # 60-90 minutes: $4.00
            cost += 4.0
        if trip['tripduration'] > 90*60:
            # Each additional 30 minutes past 90 minutes: $8.00
            addl_duration = trip['tripduration'] - 90*60
            cost += 8.0*ceil(addl_duration/(30.0*60))
        return cost

if __name__=="__main__":
    trips_by_bikeid = {}
    with open('Divvy_Trips_And_Distances_2013.csv', 'rb') as f:
        for row in csv.DictReader(f):
            trips_by_bikeid.setdefault(row['bikeid'], []).append(row)

    # This is downloaded from http://divvybikes.com/stations/json
    with open('ChicagoBikeStations.json', 'rb') as f:
        stations = json.load(f)
        latlong_by_stationname = {station['stationName']: (station['latitude'], station['longitude'])
                                    for station in stations['stationBeanList']}

    for bikeid, trips in trips_by_bikeid.iteritems():
        print('Adding lat/long, trip overage cost to data for bike {0}.'.format(bikeid))
        for trip in trips:
            trip['from_lat'], trip['from_long'] = latlong_by_stationname[trip['from_station_name']]
            trip['to_lat'], trip['to_long'] = latlong_by_stationname[trip['to_station_name']]
            trip['tripduration'] = number(trip['tripduration'])
            trip['overage'] = trip_cost(trip)
        #
        print('Writing {0} trips for bike {1}.'.format(len(trips), bikeid))
        with open(os.path.join(PATH, bikeid + '.csv'), 'wb') as f:
            dw = csv.DictWriter(f, fieldnames=sorted(trips[0].keys()))
            dw.writeheader()
            dw.writerows(sorted(trips, key=lambda trip: date(trip['starttime'])))
