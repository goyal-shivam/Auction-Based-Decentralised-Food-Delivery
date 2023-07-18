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

def dist(lat1, long1, lat2, long2):
    # returns the distance between two points by 
    # shortest distance on surface of earth
    return geopy.distance.geodesic((lat1, long1), (lat2, long2)).km

def man_dist(lat1, long1, lat2, long2):
    return dist(lat1, long1, lat2, long1) + dist(lat2, long1, lat2, long2)

data = pd.read_pickle('data/mumbai_7_days_data.pkl')
pd.options.display.max_rows = None
pd.options.display.max_columns = 4

dists = []
N = len(data)
max_dist = 0
min_dist = 1000000

points_set = set()
for i in range(N):
    points_set.add((data.iat[i,1],data.iat[i,2]))
    points_set.add((data.iat[i,3],data.iat[i,4]))

for i in points_set:
    for j in points_set:
        if(i == j):
            continue
        
        # dists.append()
        new_dist = man_dist(i[0],i[1],j[0],j[1])
        max_dist = max(max_dist,new_dist)
        min_dist = min(min_dist,new_dist)

print(N)
print(min_dist)
print(max_dist)
''' data.columns print
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
'''