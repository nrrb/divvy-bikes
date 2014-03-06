from __future__ import print_function
import csv
import os

PATH = 'trips_by_bike'

if __name__=="__main__":
    trips_by_bikeid = {}
    with open('Divvy_Trips_And_Distances_2013.csv', 'rb') as f:
        for row in csv.DictReader(f):
            trips_by_bikeid.setdefault(row['bikeid'], []).append(row)

    for bikeid, trips in trips_by_bikeid.iteritems():
        print('Writing {0} trips for bike {1}.'.format(len(trips), bikeid))
        with open(os.path.join(PATH, bikeid + '.csv'), 'wb') as f:
            dw = csv.DictWriter(f, fieldnames=trips[0].keys())
            dw.writeheader()
            dw.writerows(trips)
