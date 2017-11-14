#!/usr/bin/env python3

import json, time, tweepy
import geopy.distance

rlat = 39.4834210
rlon = -87.3248510
roseCoords = (rlat, rlon)

while True:
    with open('./dump1090/public_html/data/aircraft.json') as data_file:    
        data = json.load(data_file)
    i = 0
    for plane in data["aircraft"]:
        if "lat" in plane and "lon" in plane and "flight" in plane:
            planeCoords = (plane["lat"], plane["lon"])
            distance = geopy.distance.vincenty(roseCoords, planeCoords).miles
            print("\nPlane #",i)
            print ("lat=",plane["lat"],"lon=",plane["lon"])
            print("Distance from Rose=",distance)
            print ("flight #",plane["flight"])
        i += 1

    time.sleep(5)
    print(chr(27) + "[2J")
