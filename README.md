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

Questions
=========

# What bike has been on the most trips?

Bike 383 has helped people make 568 trips.

# What bike has travelled the farthest?

Bike 321 has travelled at least 1592238 meters or 1592 kilometers! That's some mileage for a city bike.

# What bike has been to the largest number of unique stations?

Bikes 187 and 461 tie with 193 different stations. Considering there are only 300 stations in Chicago this is 64.3% coverage.

# What bike has visited the largest number of unique stations with respect to how many trips it's made?

If a bike were to take 10 trips and if it were to be dropped off at a completely new location at the end of each trip then it could reach a maximum of 11 unique stations. In general if a bike takes N trips then the maximum number of unique stations it could reach is N+1. This is somewhat disrupted by the fact that Divvy will rebalance bike stations transporting bikes by van from a full station to one with vacancies.

There are some very young bikes (2768, 2898, 2918, 2921, 2936) that have only made one trip each and since the end station was different from where they started they each have the unbeatable ratio of 2 unique stations per trip (on average).

Let's exclude young bikes and only consider those that have been on 20 trips or more (this is totally arbitrary). Bike 1787 stands out with 51 trips and 65 unique stations. This is better than the theoretical maximum number of unique stations with rebalancing so this bike must have been rebalanced at least 13 times.

If we exclude bikes these cheating bikes and only consider those that haven't been rebalanced then we find bike 2592 that has been on 45 trips and been to 46 unique stations in that time.

# What bike has the longest average trip distance?

Bike 2918 is an unusual outlier; with only one trip to its name it traveled 6706 meters giving it the longest average trip distance.

Excluding young bikes (less than 20 trips) bike 1089 has been on 215 trips with an average distance of 3424.2 meters per trip.

# What bike has the shortest average trip distance?

# What bike has the longest average trip duration?

# What bike has the shortest average trip duration?

# What bike has the oldest average user?

# What bike has the youngest average user?

# What bike has had the greatest age diversity of users?

# What bike has generated the most revenue?

# What bike has the longest streak of days in use?

# What bike has had the greatest proportion of male/female riders?

# What bike has been most balanced between subscribers and customers?

# What bike has been most balanced in male to female riders?

# What bike has been to the most spatially diverse stations?


  [1]: https://divvybikes.com/datachallenge
  [2]: http://hubwaydatachallenge.org/
  [3]: http://divvybikes.com/pricing/Annual-Membership
  [4]: http://divvybikes.com/pricing/24-Hour-Passes