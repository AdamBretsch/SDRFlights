#!/usr/bin/env python3

import json, time, tweepy
import geopy.distance
from pprint import pprint
from weatherbit.api import Api
import Adafruit_BBIO.GPIO as GPIO

#api_key = "d2c8237889574c27a0b2e2f74a0d512e"
#api = Api(api_key)
#api.set_granularity('3hourly')



BUZZER   ="RED"

# Set the GPIO pins:
GPIO.setup(BUZZER,GPIO.OUT)

cfg = { 
    "consumer_key"        : "Gvk6OlzK9C0O7rOB0Grje1BBz",
    "consumer_secret"     : "7V9alWfWUS8O4ToCF7PAT961XymWERkUt11t9iIGUsRWpDiWJV",
    "access_token"        : "930233070011273216-v3mOZ6ofG0fxutCC9OkjrmpEUl13i2i",
    "access_token_secret" : "8uDUY7RXH6MPNhIozsFf0pzpCqZ0wZR45JTiU9Com6NM0" 
}

auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
twitter = tweepy.API(auth)
tweet = "This is a test tweet: https://elinux.org/ECE497_Project:_Local_Air_Traffic_Radio"

rlat = 39.4834210
rlon = -87.3248510
roseCoords = (rlat, rlon)
#forecast = api.get_forecast(lat=rlat,lon=rlon)
#print(forecast)

seenPlanes = [ ]
displayDistance = 50
buzzTime = 1

while True:
    with open('./dump1090/public_html/data/aircraft.json') as data_file:    
        data = json.load(data_file)
    i = 0
    for plane in data["aircraft"]:
        if "lat" in plane and "lon" in plane and "flight" in plane and "altitude" in plane and "speed" in plane:
            planeCoords = (plane["lat"], plane["lon"])
            distance = geopy.distance.vincenty(roseCoords, planeCoords).miles
            if plane["flight"] not in seenPlanes:
                if distance < displayDistance:
                    dis = str(int(distance*1000)/1000.0)
                    flight = str(plane["flight"])
                    flight = ''.join(flight.split())
                    speed = str(plane["speed"])
                    alt = str(plane["altitude"])
                    tweet = "Flight #"+flight+" spotted "+dis+" miles from Rose-Hulman, traveling "+speed+" mph at "+alt+" ft http://flightaware.com/live/flight/"+flight
                    print(tweet)
                    status = twitter.update_status(status=tweet)
                    GPIO.output(BUZZER, 1)
                    time.sleep(buzzTime)
                    GPIO.output(BUZZER,0)
                    seenPlanes.append(plane["flight"])

    time.sleep(1)
