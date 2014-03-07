from __future__ import print_function
from datetime import datetime
import json
import csv
import os

PATH = './trips_by_bike/'

def date(date_string):
    return datetime.strptime(date_string, '%m/%d/%Y %H:%M')


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
        print('Adding lat/long to data for bike {0}.'.format(bikeid))
        for trip in trips:
            trip['from_lat'], trip['from_long'] = latlong_by_stationname[trip['from_station_name']]
            trip['to_lat'], trip['to_long'] = latlong_by_stationname[trip['to_station_name']]
        #
        print('Writing {0} trips for bike {1}.'.format(len(trips), bikeid))
        with open(os.path.join(PATH, bikeid + '.csv'), 'wb') as f:
            dw = csv.DictWriter(f, fieldnames=sorted(trips[0].keys()))
            dw.writeheader()
            dw.writerows(sorted(trips, key=lambda trip: date(trip['starttime'])))
