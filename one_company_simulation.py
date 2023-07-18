# Decentralised simulation
import pandas as pd
from pprint import pprint
from matplotlib import pyplot as plt
# import pickle
from collections import Counter
import geopy.distance
import simpy
from random import randrange
from math import ceil
import numpy as np
import pickle as pkl

NUM_BOYS = 15  # 20 maybe
NUM_BOYS_PER_COMPANY = 3 # 4 maybe
NUM_OF_COMPANIES = 5
BIKE_SPEED = 20 # 25 maybe

BOYS = []
LOG_DATA = []
ORDER_DATA = [] # distance, time
QUEUE_LENGTH = 0

MAX_LAT, MIN_LAT, MAX_LONG, MIN_LONG = 0,0,0,0

def dist(lat1, long1, lat2, long2):
    # returns the distance between two points by 
    # shortest distance on surface of earth
    return geopy.distance.geodesic((lat1, long1), (lat2, long2)).km

def man_dist(lat1, long1, lat2, long2):
    return dist(lat1, long1, lat2, long1) + dist(lat2, long1, lat2, long2)

def get_index_of_nearest_boy(lat,long,time_now):
    min_time = 1000000000
    min_ind = -1

    for i in range(NUM_BOYS):
        new_time = BOYS[i]['free_at']
        if(BOYS[i]['free_at'] <= time_now):
            new_time = time_now
        new_time += ceil(man_dist(lat, long, BOYS[i]['lat'], BOYS[i]['long'])/BIKE_SPEED)
        if(min_time > new_time):
            min_ind = i
            min_time = new_time

    return min_ind

def save_data(curr_time):
    if(len(LOG_DATA)==0):
        LOG_DATA.append((curr_time, QUEUE_LENGTH))
    elif (LOG_DATA[-1][0] == curr_time):
        LOG_DATA[-1] = (LOG_DATA[-1][0], QUEUE_LENGTH)
    else:
        time = LOG_DATA[-1][0]
        val = LOG_DATA[-1][1]
        while(LOG_DATA[-1][0] < curr_time-1):
            time += 1
            LOG_DATA.append((time, val))
            # print('.', end='')
        LOG_DATA.append((curr_time, QUEUE_LENGTH))
        # print()

data = pd.read_pickle('data/mumbai_7_days_data.pkl')
pd.options.display.max_rows = None
pd.options.display.max_columns = 4

a = 'Restaurant_latitude'
b = 'Delivery_location_latitude'
c = 'Restaurant_longitude'
d = 'Delivery_location_longitude'

MAX_LAT = max(data[a].max(), data[b].max())
MIN_LAT = min(data[a].min(), data[b].min())
MAX_LONG = max(data[c].max(), data[d].max())
MIN_LONG = min(data[c].min(), data[d].min())
N = len(data)




for i in range(NUM_BOYS):
    BOYS.append({'lat':randrange(10001), 'long':randrange(10001)})

for i in range(NUM_BOYS):
    BOYS[i]['lat'] = MIN_LAT + (MAX_LAT - MIN_LAT)*BOYS[i]['lat']/10000
    BOYS[i]['long'] = MIN_LONG + (MAX_LONG - MIN_LONG)*BOYS[i]['long']/10000
    BOYS[i]['free_at'] = 0

'''
if BOYS['free_in'] == 0:
    then it means that the location of the boy is at it lat, long. else if the free_in has some value, it means that at free_at time in the simulation environment in minutes, the boy will become free, and then it's location will become equal to lat,long which is currently stored in it's entry

to check if boy is free or not, you can simply check whether his free_at is less than or equal to current time of simulation or not. if yes, he is free, else he is busy right now and will become free at his free_at time.

free_at means boy is free at the starting edge of that minute
'''

''' data.columns print, min_dist, max_dist, N, freq per day
0 ID
1 Restaurant_latitude
2 Restaurant_longitude
3 Delivery_location_latitude
4 Delivery_location_longitude
5 Order_Date
6 Time_Orderd
7 Time_Order_picked
8 Time_taken(min)
9 order_pick
10 order_place
11 order_delivered

N = 2872
min_dist = 0.05763515594883869
max_dist = 66.00012665542367

{datetime.date(2022, 4, 1): 375,
 datetime.date(2022, 4, 2): 429,
 datetime.date(2022, 4, 3): 408,
 datetime.date(2022, 4, 4): 531,
 datetime.date(2022, 4, 5): 333,
 datetime.date(2022, 4, 6): 467,
 datetime.date(2022, 4, 7): 329}

'''

def customer_generator(env, boys):
    global data, N
    
    for i in range(N):
        if(i == 0):
            t = 0
        else:
            t = (data.iat[i,10]-data.iat[i-1,10]).total_seconds()/60

        yield env.timeout(ceil(t))

        c = Customer(
            env=env,
            boys=boys,
            name=f'Customer {i+1}',
            res_lat=data.iat[i,1],
            res_long=data.iat[i,2],
            client_lat=data.iat[i,3],
            client_long=data.iat[i,4]
        )

        env.process(c.action())


env = simpy.Environment()
boys = simpy.Resource(env, NUM_BOYS)
env.process(customer_generator(env, boys))

env.run()