from collections import defaultdict
from datetime import datetime
import csv
from math import ceil

def date(date_string):
	return datetime.strptime(date_string, '%m/%d/%Y %H:%M')

def number(int_string):
	return int(int_string.replace(',', ''))

def bike_trips(bike_id):
	return filter(lambda trip: trip['bikeid']==bike_id, trips)

def visited_stations(trips):
	from_stations = [trip['from_station_id'] for trip in trips]
	to_stations = [trip['to_station_id'] for trip in trips]
	return set(from_stations + to_stations)

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
			addl_duration = trip['tripduration'] - 90*60
			cost += 6.0*ceil(addl_duration/30.)
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
			addl_duration = trip['tripduration'] - 90*60
			cost += 8.0*ceil(addl_duration/30.)
		return cost

with open('Divvy_Trips_And_Distances_2013.csv', 'rb') as f:
	trips = list(csv.DictReader(f))

bikeids = set()
trips_by_bike = defaultdict(lambda: 0)
distance_by_bike = defaultdict(lambda: 0)
stations_by_bike = defaultdict(lambda: set())
duration_by_bike = defaultdict(lambda: 0)
ages_by_bike = defaultdict(lambda: [])
revenue_by_bike = defaultdict(lambda: 0)
avg_trip_distance_by_bike = {}
avg_trip_duration_by_bike = {}
avg_age_by_bike = {}
age_range_by_bike = {}

for trip in trips:
	# Cleaning the data
	trip['starttime'] = date(trip['starttime'])
	trip['stoptime'] = date(trip['stoptime'])
	trip['tripduration'] = number(trip['tripduration'])
	trip['meters'] = int(trip['meters'])
	if trip['birthyear'] != '':
		trip['birthyear'] = int(trip['birthyear'])
	# Aggregation
	bikeids.add(trip['bikeid'])
	trips_by_bike[trip['bikeid']] += 1
	distance_by_bike[trip['bikeid']] += trip['meters']
	stations_by_bike[trip['bikeid']].add(trip['from_station_id'])
	stations_by_bike[trip['bikeid']].add(trip['to_station_id'])
	duration_by_bike[trip['bikeid']] += trip['tripduration']
	if trip['birthyear'] != '':
		ages_by_bike[trip['bikeid']].append(2014-trip['birthyear'])
	revenue_by_bike[trip['bikeid']] += trip_cost(trip)

for bikeid, stations in stations_by_bike.iteritems():
	stations_by_bike[bikeid] = len(stations)

for bikeid in distance_by_bike:
	avg_trip_distance_by_bike[bikeid] = (float(distance_by_bike[bikeid]) /
										 float(trips_by_bike[bikeid]))
	avg_trip_duration_by_bike[bikeid] = (float(duration_by_bike[bikeid]) /
										 float(trips_by_bike[bikeid]))
	if len(ages_by_bike[bikeid]) > 0:
		avg_age_by_bike[bikeid] = (float(sum(ages_by_bike[bikeid])) /
								   float(len(ages_by_bike[bikeid])))
		age_range_by_bike[bikeid] = max(ages_by_bike[bikeid]) - min(ages_by_bike[bikeid])

# Write out data to CSV
with open('stats_by_bike.csv', 'wb') as f:
	fields = ['bikeid', 'trips', 'distance', 'stations', 'duration',
				'avg_trip_distance', 'avg_trip_duration', 'avg_age',
				'age_range', 'revenue']
	dw = csv.DictWriter(f, fieldnames=fields)
	dw.writeheader()
	for bikeid in sorted(list(bikeids)):
		dw.writerow({
				'bikeid': bikeid,
				'trips': trips_by_bike[bikeid],
				'distance': distance_by_bike[bikeid],
				'stations': stations_by_bike[bikeid],
				'duration': duration_by_bike[bikeid],
				'avg_trip_distance': round(avg_trip_distance_by_bike[bikeid], 1),
				'avg_trip_duration': round(avg_trip_duration_by_bike[bikeid], 1),
				'avg_age': round(avg_age_by_bike.get(bikeid, -1), 1),
				'age_range': round(age_range_by_bike.get(bikeid, -1), 1),
				'revenue': round(revenue_by_bike[bikeid], 2)
			})

# What bike has been on the most trips?
print "What bike has been on the most trips?"
print "bikeid {0}, {1} trips".format(
		*max(trips_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 383, 568 trips

# What bike has travelled the farthest?
print "What bike has travelled the farthest?"
print "bikeid {0}, {1} meters".format(
		*max(distance_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 321, 1592238 meters

# What bike has been to the largest number of unique stations?
print "What bike has been to the largest number of unique stations?"
print "bikeid {0}, {1} stations".format(
		*max(stations_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 187, 193 stations

# What bike has the longest average trip distance?
print "What bike has the longest average trip distance?"
print "bikeid {0}, {1} average meters per trip".format(
		*max(avg_trip_distance_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 2918, 6706.0 average meters per trip

# What bike has the shortest average trip distance?
print "What bike has the shortest average trip distance?"
print "bikeid {0}, {1} average meters per trip".format(
		*min(avg_trip_distance_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 2810, 0.0 average meters per trip

# What bike has the longest average trip duration?
print "What bike has the longest average trip duration?"
print "bikeid {0}, {1} seconds average trip duration".format(
		*max(avg_trip_duration_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 2779, 7902.5 seconds average trip duration

# What bike has the shortest average trip duration?
print "What bike has the shortest average trip duration?"
print "bikeid {0}, {1} seconds average trip duration".format(
		*min(avg_trip_duration_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 2810, 133.0 seconds average trip duration

# What bike has the oldest average user?
print "What bike has the oldest average user?"
print "bikeid {0}, {1} years old".format(
		*max(avg_age_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 2936, 63.0 years old

# What bike has the youngest average user?
print "What bike has the youngest average user?"
print "bikeid {0}, {1} years old".format(
		*min(avg_age_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 2761, 23.5 years old

# What bike has had the greatest age diversity of users?
print "What bike has had the greatest age diversity of users?"
print "bikeid {0}, {1} years from youngest to oldest user".format(
		*max(age_range_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 683, 91 years from youngest to oldest user

# What bike has generated the most revenue?
print "What bike has generated the most revenue?"
print "bikeid {0}, ${1}".format(
		*max(revenue_by_bike.iteritems(), key=lambda x: x[1])
	)
# bikeid 520, $68230.0

# What bike has the longest streak of days in use?
# What bike has had the greatest proportion of male/female riders?
# What bike has been most balanced between subscribers and customers?
# What bike has been most balanced in male to female riders?
# What bike has been to the most spatially diverse stations?
