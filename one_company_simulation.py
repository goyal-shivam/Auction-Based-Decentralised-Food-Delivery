# Decentralised simulation
import pandas as pd
from pprint import pprint
from matplotlib import pyplot as plt
# import pickle
from collections import Counter
import geopy.distance
import simpy
import random
from math import ceil
import numpy as np
import pickle as pkl

NUM_BOYS_PER_COMPANY = 10 # 4 maybe
NUM_OF_COMPANIES = 20
NUM_BOYS = NUM_BOYS_PER_COMPANY * NUM_OF_COMPANIES # 20 maybe
BIKE_SPEED = 40

K_MEANS_DIST = 4
AUCTION_K = 5

BOYS = []
LOG_DATA = []
ORDER_DATA = [] # distance, time
NUM_CUSTOMERS = 0
K_MEANS_DATA = []

MAX_LAT, MIN_LAT, MAX_LONG, MIN_LONG = 0,0,0,0

data = None

def dist(lat1, long1, lat2, long2):
    # returns the distance between two points by 
    # shortest distance on surface of earth
    return geopy.distance.geodesic((lat1, long1), (lat2, long2)).km

def man_dist(lat1, long1, lat2, long2):
    return dist(lat1, long1, lat2, long1) + dist(lat2, long1, lat2, long2)

def min_bid (order):
    return order * 0.1

def max_bid (order):
    return order * 0.2

def machine_predicted_bid(rider_ind, order_cost):
    # rider_ind is the index of the delivery boy in the BOYS array
    pass

def first_bid (machine_bid, order):
    a = (machine_bid - min_bid(order)) * 2 + min_bid(order)
    if a < max_bid(order):
        return random.randint(a, max_bid(order))
    else:
        return max_bid(order)
    
def second_bid (machine_bid, order):
#     print(machine_bid)
    a = first_bid(machine_bid, order)
#     print(a)
    return random.randint(machine_bid + 1, a)

def third_bid (machine_bid, order):
    return random.randint(int(machine_bid / 1.5), machine_bid)

def customer_rating(order_num, rider_ind, order_cost):
    rating = None

    return rating

def update_rider_rating(customer_rating, wait_time, dist_between_rest_and_cust):
    pass

def simulate_restaurant_owner(bids_df, order_cost):
    


    return bids_df

def perform_auction(riders_ind_list, order_cost):
    min_bid_res = []
    max_bid_res = []
    first_bid_res = []
    second_bid_res = []
    third_bid_res = []
    ratings = []

    for i in riders_ind_list:
        min_bid_res.append(min_bid(order_cost))
        max_bid_res.append(max_bid(order_cost))
        first_bid_res.append(first_bid(i,order_cost))
        second_bid_res.append(second_bid(i,order_cost))
        third_bid_res.append(third_bid(i,order_cost))
        ratings.append(BOYS[i]['rating'])

    bids = {
        'rider_ind' : riders_ind_list, 
        'first_bid': first_bid_res, 
        'second_bid': second_bid_res, 
        'third_bid': third_bid_res,
        'rider_rating': ratings
        }
    
    bids_df = pd.DataFrame(bids)
    bids_df.set_index('rider_ind', drop=False, inplace=True)
    bids_df = simulate_restaurant_owner(bids_df, order_cost, min_bid, max_bid)

    chosen_rider = random.choices(list(bids_df['rider_ind']), weights=list(bids_df['selection_prob']))

    delivery_charges = random.choices(
        [
            bids_df[chosen_rider]['first_bid'],
            bids_df[chosen_rider]['second_bid'],
            bids_df[chosen_rider]['third_bid'],
        ],
        weights=[1,9,90]
        # weights=[10,20,70]
    )
    
    return chosen_rider, delivery_charges

def get_index_of_nearest_boy(lat,long,time_now,order_num):
    min_time = 1000000000
    min_ind = -1
    dist_corresponding_to_min = 1000000000
    
    global K_MEANS_DATA
    nearby_bikers = 0

    for i in range(NUM_BOYS):
        new_time = BOYS[i]['free_at']
        if(BOYS[i]['free_at'] <= time_now):
            new_time = time_now
        dist = man_dist(lat, long, BOYS[i]['lat'], BOYS[i]['long'])

        new_time += ceil((dist/BIKE_SPEED)*60)

        if(new_time-time_now<=ceil((K_MEANS_DIST/BIKE_SPEED)*60)):
           nearby_bikers += 1
           
        if(min_time > new_time):
            min_ind = i
            min_time = new_time
            dist_corresponding_to_min = dist

    K_MEANS_DATA.append((order_num, nearby_bikers))
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




for i in range(NUM_BOYS):
    BOYS.append({'lat':random.randrange(10001), 'long':random.randrange(10001)})

for i in range(NUM_BOYS):
    BOYS[i]['lat'] = MIN_LAT + (MAX_LAT - MIN_LAT)*BOYS[i]['lat']/10000
    BOYS[i]['long'] = MIN_LONG + (MAX_LONG - MIN_LONG)*BOYS[i]['long']/10000
    BOYS[i]['free_at'] = 0

''' free_in explanation
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
    def __init__(self, env, boys, name, res_lat, res_long, client_lat, client_long, order_num):
        self.env = env
        self.boys = boys
        self.name = name
        self.res_lat = res_lat
        self.res_long = res_long
        self.client_lat = client_lat
        self.client_long = client_long

        self.bike_ind = None
        self.bike_reach_restaurant_at = None
        self.start_time = 0

        self.order_num = order_num

    def action(self):
        global NUM_CUSTOMERS, ORDER_DATA

        NUM_CUSTOMERS += 1
        save_data(self.env.now)

        self.start_time = self.env.now

        self.bike_ind, self.bike_reach_restaurant_at, dist1 = get_index_of_nearest_boy(self.res_lat, self.res_long, self.env.now, self.order_num)

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
        ORDER_DATA.append((dist1+dist2, self.env.now-self.start_time))
        print(f'{self.order_num}, ', end='',flush=True)


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
            client_long=data.iat[i,4],
            order_num=i
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

with open(f"data/{dataset_acronym}_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_decent.pkl", 'wb') as file:
    pkl.dump((x,y), file)

with open(f"data/{dataset_acronym}_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_ORDER_DATA.pkl", 'wb') as file:
    pkl.dump(ORDER_DATA, file)

with open(f"data/{dataset_acronym}_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_K_DIST_{K_MEANS_DIST}_K_MEANS_DATA.pkl", 'wb') as file:
    pkl.dump(K_MEANS_DATA, file)




plt.figure('Queue Length vs Time Decentralised One company')
plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
plt.plot(x,y, color='#fc5c65')

plt.axhline(np.average(y),0, np.amax(x), color='#576574')
print(f'\nDecentralised average queue length is {np.average(y)}\nNUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}\n')

plt.show()