The Real Stars of Divvy: The Bikes
----------------------------------

Background
==========

Divvy Bikes operates an urban bike sharing system in Chicago
 IL in cooperation with Chicago Department of Transportation (CDOT). They released a set of data representing all bike trips taken in the system since original deployment in July 2013. This is part of the [Divvy Data Challenge][1]
 a competition they are sponsoring to do something interesting with the data.

They've done [a similar challenge in Boston][2]
 where there were 67 submissions telling a variety of stories using the data. The predominant narrative was from the perspective of the users of the system
 those people riding the bikes. There is a vacuum in the space of telling stories from the perspectives of the bikes themselves.

What's In The Data
==================

There are 759788 trips rows in the data file provided by Divvy. Each trip includes the following fields:

1. **trip_id** - Unique ID number per trip, ranging from 3940 to 1109397
2. **starttime** - Date and time that the trip started, in the format mm/dd/yyyy hh:mm. For example, "6/27/2013 12:11".
3. **stoptime** - Date and time that the trip ended, in the format mm/dd/yyyy hh:mm. For example, "6/27/2013 12:16".
4. **bikeid** - Unique ID for each bike in the Divvy bike fleet. There are 2887 unique IDs, ranging from 1 to 3003. 
5. **tripduration** - How long the trip was, in seconds. This field is numeric, but **NOTE** that there is a comma as a thousands separator. For example, trip_id 27 has a tripduration of "10,105". 
6. **from_station_id** - Unique ID for each Divvy bike station, where the trip started. There are 300 total Divvy stations, and every one of these appears as a **from_station_id**. They range from 1 to 440. **NOTE**: the "Congress Pkwy & Ogden Ave" station appears with the ID "#N/A".
7. **from_station_name** - The unique name of the Divvy bike station where the trip started. There are 300 total Divvy station names and each one appears at least once in this field. Example: "Southport Ave & Wrightwood Ave"
8. **to_station_id** - Unique ID for each Divvy bike station, where the trip ended. There are 300 total Divvy stations, and every one of these appears as a **to_station_id**. They range from 1 to 440. **NOTE**: the "Congress Pkwy & Ogden Ave" station appears with the ID "#N/A".
9. **to_station_name** - The unique name of the Divvy bike station where the trip ended. There are 300 total Divvy station names and each one appears at least once in this field. Example: "Southport Ave & Wrightwood Ave"
10. **usertype** - This represents whether the trip was taken by a Divvy subscriber, someone who has paid for the [yearly membership][3], or by a one-time customer who bought [a 24-hour pass][4]. Subscriber trips are represented as "Subscriber" and customer trips are represented as "Customer".
11. **gender** - If the trip was taken by a Divvy Subscriber, and the subscriber chose to report their gender (it is optional), then this will report the gender of the rider as "Male" or "Female". Otherwise, this field is blank ("").
12. **birthyear** - If the trip was taken by a Divvy Subscriber, and the subscriber chose to report their birth year (it is optional), then this will be filled in. If the Subscriber did not fill out their birth year, or if it is a Customer trip, then this will be blank (""). Values range from 1906 to 1997. 

For each of the bike trip data points provided for the Chicago data set the unique bike ID is provided. Using this ID we can aggregate statistics by bike and showcase the notable bikes.

## Adding Station-to-Station Estimated Distances

Steve Vance munged the data, combining it with station-to-station distances to approximate (or put a lower bound on) the length of the trip, and [provides it for download as CSV and SQL](https://github.com/stevevance/divvy-munging). This is were I got `Divvy_Trips_And_Distances_2013.csv.zip` from. Thank you, Steve, for merging and providing this data!

## Derived Data

[read_csv.py](https://github.com/tothebeat/divvy-bikes/blob/master/read_csv.py) also creates a file [stats_by_bike.csv](https://github.com/tothebeat/divvy-bikes/blob/master/stats_by_bike.csv) that has 2887 rows, one for each bike, and the following fields for each bike:

* trips - number of trips taken by the bike.
* distance - total distance travelled by the bike, a sum of the individual trip estimated distances. note that this is a lower bound.
* stations - number of unique stations the bike has been to.
* trips/station - basically the trips field divided by the stations field. this is useful when considering diversity of stations with respect to a bike's overall activity.
* duration - total time the bike has been used.
* avg_trip_distance - the total distance divided by the total number of trips.
* avg_trip_duration - the total duration divided by the total number of trips.
* avg_age - The average age of the rider, based on the trips taken by Divvy Subscribers for whom the age was recorded.
* age_range - The number of years between the age of the youngest rider and the oldest rider of the bike.
* revenue - The revenue generated by the bike based on overage charges, taking into account whether a Subscriber or Daily Pass rider was using it. This is in US Dollars.

## Data Files By Bike ID

I [created individual CSV files](https://github.com/tothebeat/divvy-bikes/blob/master/split_trips_by_bike.py) per bikeid with all of the trips the bike took as rows. For instance, all trips taken by the bike with ID 383 are in [https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/383.csv](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/383.csv).

Questions
=========

## What bike has been on the most trips?

Bike [383](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/383.csv) has helped people make 568 trips.

## What bike has travelled the farthest?

Bike [321](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/321.csv) has travelled at least 1592238 meters or 1592 kilometers! That's some mileage for a city bike.

## What bike has been to the largest number of unique stations?

Bikes [187](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/187.csv) and [461](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/461.csv) tie with 193 different stations. Considering there are only 300 stations in Chicago this is 64.3% coverage.

## What bike has visited the largest number of unique stations with respect to how many trips it's made?

If a bike were to take 10 trips and if it were to be dropped off at a completely new location at the end of each trip then it could reach a maximum of 11 unique stations. In general if a bike takes N trips then the maximum number of unique stations it could reach is N+1. This is somewhat disrupted by the fact that Divvy will rebalance bike stations transporting bikes by van from a full station to one with vacancies.

There are some very young bikes ([2768](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2768.csv), [2898](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2898.csv), [2918](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2918.csv), [2921](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2921.csv), [2936](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2936.csv)) that have only made one trip each and since the end station was different from where they started they each have the unbeatable ratio of 2 unique stations per trip (on average).

Let's exclude young bikes and only consider those that have been on 20 trips or more (this is totally arbitrary). Bike [1787](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/1787.csv) stands out with 51 trips and 65 unique stations. This is better than the theoretical maximum number of unique stations with rebalancing so this bike must have been rebalanced at least 13 times.

If we exclude bikes these cheating bikes and only consider those that haven't been rebalanced then we find bike [2592](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2592.csv) that has been on 45 trips and been to 46 unique stations in that time.

## What bike has the longest average trip distance?

Bike [2918](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2918.csv) is an unusual outlier; with only one trip to its name it traveled 6706 meters giving it the longest average trip distance.

Excluding young bikes (less than 20 trips), bike [1089](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/1089.csv) has been on 215 trips with an average distance of 3424.2 meters per trip.

## What bike has the shortest average trip distance?

## What bike has the longest average trip duration?

Bike [2779](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2779.csv) has only 4 trips in its pedigree but averages 7902.5 seconds per trip. This is because of one trip that lasted 30919 seconds; someone picked up this bike at 11:29pm on December 20, 2013 and returned it to a station 2 kilometers away at 8:04am the next day (December 21). My guess is that, instead of someone riding very very slowly, probably the rider went to sleep and bike [2779](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2779.csv) waited faithfully outside.

Excluding young bikes (less than 20 trips), bike [2452](https://github.com/tothebeat/divvy-bikes/blob/master/trips_by_bike/2452.csv) has been on 55 trips with an average duration of 3134.7 seconds per trip.

## What bike has the shortest average trip duration?

## What bike has the oldest average user?

## What bike has the youngest average user?

## What bike has had the greatest age diversity of users?

## What bike has generated the most revenue?

## What bike has the longest streak of days in use?

## What bike has had the greatest proportion of male/female riders?

## What bike has been most balanced between subscribers and customers?

## What bike has been most balanced in male to female riders?

## What bike has been to the most spatially diverse stations?


  [1]: https://divvybikes.com/datachallenge
  [2]: http://hubwaydatachallenge.org/
  [3]: http://divvybikes.com/pricing/Annual-Membership
  [4]: http://divvybikes.com/pricing/24-Hour-Passes
