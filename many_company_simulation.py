# Centralised simulation
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
import random

NUM_BOYS_PER_COMPANY = 10 # 4 maybe
NUM_OF_COMPANIES = 20
NUM_BOYS = NUM_BOYS_PER_COMPANY * NUM_OF_COMPANIES # 20 maybe
BIKE_SPEED = 40

AVERAGE_RIDER_RATING = 2500
AVERAGE_CUSTOMER_RATING = 2.5
NUM_ORDERS_DONE = 0

BOYS = []
LOG_DATA = []
ORDER_DATA = [] # distance, time
DELIVERY_CHARGES_RATING = [] # delivery_charges, rating by customer
NUM_CUSTOMERS = 0

MAX_LAT, MIN_LAT, MAX_LONG, MIN_LONG = 0,0,0,0

def dist(lat1, long1, lat2, long2):
    # returns the distance between two points by 
    # shortest distance on surface of earth
    return geopy.distance.geodesic((lat1, long1), (lat2, long2)).km

def man_dist(lat1, long1, lat2, long2):
    return dist(lat1, long1, lat2, long1) + dist(lat2, long1, lat2, long2)

def min_bid (order):
    return ceil(order * 0.1)

def max_bid (order):
    return ceil(order * 0.2)

def dist_travelled(rider_ind, lat, long, client_lat, client_long):
    global BOYS

    total_dist = 0
    total_dist += ceil(man_dist(BOYS[i]['lat'], BOYS[i]['long'], lat, long))
    total_dist += ceil(man_dist(lat, long, client_lat, client_long))

    return total_dist

def machine_predicted_bid(total_dist, order_cost):
    # rider_ind is the index of the delivery boy in the BOYS array
    
    min_bid_res = min_bid(order_cost)
    max_bid_res = max_bid(order_cost)

    return ceil((max_bid_res - min_bid_res)*0.5*total_dist/40) + min_bid_res

def customer_rating(actual_wait_time, min_wait_time):
    '''
    actual_wait_time is the time that the customer had to wait to receive the order after placing the order
    min_wait_time is the time required for the delivery boy to travel from restaurant to client location
    '''

    # here 10-1 in the formula specifies that when wait_time is 10 times the minimum possible, the rating is 2.5
    return 5*(np.exp(-((actual_wait_time-min_wait_time)/min_wait_time/(10-1)*np.log(2))))

def update_rider_rating(customer_rating, rider_ind):
    global AVERAGE_RIDER_RATING, AVERAGE_CUSTOMER_RATING, NUM_ORDERS_DONE, BOYS

    older_rating = BOYS[rider_ind]['rating']

    e = 1/(1+10**((AVERAGE_RIDER_RATING-older_rating)/800))
    change = 32*((1 if customer_rating > AVERAGE_CUSTOMER_RATING*0.8 else 0)-e)

    BOYS[rider_ind]['rating'] = older_rating + change

    AVERAGE_CUSTOMER_RATING = (AVERAGE_CUSTOMER_RATING*NUM_ORDERS_DONE + customer_rating)/(NUM_ORDERS_DONE + 1)
    NUM_ORDERS_DONE += 1

    AVERAGE_RIDER_RATING = ((NUM_BOYS*AVERAGE_RIDER_RATING) + change)/NUM_BOYS

def get_index_of_nearest_boy(lat,long,company,time_now):
    global NUM_BOYS_PER_COMPANY
    min_time = 1000000000
    min_ind = -1
    dist_corresponding_to_min = 1000000000

    for i in range(company*NUM_BOYS_PER_COMPANY, (company+1)*NUM_BOYS_PER_COMPANY):
        new_time = BOYS[i]['free_at']
        if(BOYS[i]['free_at'] <= time_now):
            new_time = time_now
        dist = man_dist(lat, long, BOYS[i]['lat'], BOYS[i]['long'])

        new_time += ceil((dist/BIKE_SPEED)*60)
        if(min_time > new_time):
            min_ind = i
            min_time = new_time
            dist_corresponding_to_min = dist

    return min_ind, min_time, dist_corresponding_to_min

def save_data(curr_time):
    if(len(LOG_DATA)==0):
        LOG_DATA.append((curr_time, NUM_CUSTOMERS))
    elif (LOG_DATA[-1][0] == curr_time):
        LOG_DATA[-1] = (LOG_DATA[-1][0], NUM_CUSTOMERS)
    else:
        time = LOG_DATA[-1][0]
        val = LOG_DATA[-1][1]
        while(LOG_DATA[-1][0] < curr_time-1):
            time += 1
            LOG_DATA.append((time, val))
            # print('.', end='')
        LOG_DATA.append((curr_time, NUM_CUSTOMERS))
        # print()


data, dataset_acronym = pd.read_pickle('data/mumbai_all_in_one_day.pkl'), 'ONEDAY'
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

def get_company_allot():
    global N, NUM_OF_COMPANIES

    company_allot = list(range(0, N))
    company_allot = list(map(lambda x:x%NUM_OF_COMPANIES, company_allot))

    company_allot = np.array(company_allot)
    np.random.shuffle(company_allot)

    return company_allot



for i in range(NUM_BOYS):
    BOYS.append({'lat':randrange(10001), 'long':randrange(10001)})

for i in range(NUM_BOYS):
    BOYS[i]['lat'] = MIN_LAT + (MAX_LAT - MIN_LAT)*BOYS[i]['lat']/10000
    BOYS[i]['long'] = MIN_LONG + (MAX_LONG - MIN_LONG)*BOYS[i]['long']/10000
    BOYS[i]['free_at'] = 0
    BOYS[i]['rating'] = 2500

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

class Customer:
    def __init__(self, env, boys, name, res_lat, res_long, client_lat, client_long, company, order_num, order_cost):
        self.env = env
        self.boys = boys
        self.name = name
        self.res_lat = res_lat
        self.res_long = res_long
        self.client_lat = client_lat
        self.client_long = client_long
        self.order_cost = order_cost

        self.bike_ind = None
        self.bike_reach_restaurant_at = None
        self.company = company
        self.start_time = 0

        self.order_num = order_num

    def action(self):
        global NUM_CUSTOMERS, ORDER_DATA, DELIVERY_CHARGES_RATING

        NUM_CUSTOMERS += 1
        save_data(self.env.now)

        self.start_time = self.env.now

        self.bike_ind, self.bike_reach_restaurant_at, dist1 = get_index_of_nearest_boy(self.res_lat, self.res_long, self.company, env.now)

        yield env.timeout(self.bike_reach_restaurant_at - self.env.now)

        dist2 = man_dist(self.client_lat, self.client_long, self.res_lat, self.res_long)

        time2 = ceil((dist2/BIKE_SPEED)*60)

        # update boy's coordinates
        BOYS[self.bike_ind]['lat'] = self.client_lat
        BOYS[self.bike_ind]['long'] = self.client_long
        BOYS[self.bike_ind]['free_at'] = self.bike_reach_restaurant_at + time2

        yield self.env.timeout(time2)

        NUM_CUSTOMERS -= 1
        save_data(self.env.now)
        actual_wait_time = self.env.now-self.start_time
        ORDER_DATA.append((dist1+dist2, actual_wait_time))
        rating_by_customer = customer_rating(actual_wait_time, time2)
        DELIVERY_CHARGES_RATING.append((machine_predicted_bid(self.bike_ind, self.order_cost), rating_by_customer))
        update_rider_rating(rating_by_customer, self.bike_ind)
        print(f'{self.order_num}, ', end='',flush=True)


def customer_generator(env, boys):
    global data, N

    company_allot = get_company_allot()
    
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
            client_long=data.iat[i,4],
            company=company_allot[i],
            order_num=i,
            order_cost=data.iat[i,27]
        )

        env.process(c.action())


env = simpy.Environment()
boys = simpy.Resource(env, NUM_BOYS)
env.process(customer_generator(env, boys))

env.run()



x = []
y = []

for i in LOG_DATA:
    # print(i)
    x.append(i[0])
    y.append(i[1])

x = np.array(x)
y = np.array(y)

with open(f"data/{dataset_acronym}_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_centralised.pkl", 'wb') as file:
    pkl.dump((x,y), file)

with open(f"data/{dataset_acronym}_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_ORDER_DATA_centralised.pkl", 'wb') as file:
    pkl.dump(ORDER_DATA, file)

with open(f"data/{dataset_acronym}_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_DELIVERY_CHARGES_RATING_centralised.pkl", 'wb') as file:
    pkl.dump(DELIVERY_CHARGES_RATING, file)




plt.figure('Queue Length vs Time Centralised Many companies')
plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
plt.plot(x,y, color='#a55eea')

plt.axhline(np.average(y),0, np.amax(x), color='#222f3e')
print(f'\nCentralised average queue length is {np.average(y)}\nNUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}\n')

plt.show()