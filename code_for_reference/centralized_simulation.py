import geopy.distance
import pandas as pd
import simpy
from random import randrange
from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

# data = pd.read_pickle('data_1000.pkl')
data = pd.read_pickle('data_preprocessed.pkl')

MAX_LAT = 0
MIN_LAT = 0
MAX_LONG = 0
MIN_LONG = 0
NUM_BOYS = 100
NUM_BOYS_PER_COMPANY = 5
NUM_OF_COMPANIES = ceil(NUM_BOYS/NUM_BOYS_PER_COMPANY)
BIKE_SPEED = 40
NUM_CUSTOMERS = 0
BOYS = []
LOG_DATA = []
ORDER_DATA = [] # distance, time

def dist(lat1, long1, lat2, long2):
    # returns the distance between two points by 
    # shortest distance on surface of earth
    return geopy.distance.geodesic((lat1, long1), (lat2, long2)).km

def man_dist(lat1, long1, lat2, long2):
    return dist(lat1, long1, lat2, long1) + dist(lat2, long1, lat2, long2)

def get_index_of_nearest_boy(lat,long,company,time_now):
    min_time = 1000000000
    min_ind = -1
    for i in range(company*NUM_BOYS_PER_COMPANY,(company+1)*NUM_BOYS_PER_COMPANY,1):
        new_time = BOYS[i]['busy']
        if(BOYS[i]['busy'] == 0):
            new_time += time_now

        new_time += ceil(man_dist(lat, long, BOYS[i]['lat'], BOYS[i]['long'])/BIKE_SPEED*60)
        if(min_time > new_time):
            min_ind = i
            min_time = new_time

    return min_ind

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

def customer_generator(env, companies):
    global data

    company_allot = []
    count = 0
    for i in range(data.shape[0]):
        company_allot.append(count)
        
        if count == NUM_OF_COMPANIES-1:
            count = 0   
        else:
            count += 1

    company_allot = np.array(company_allot)
    np.random.shuffle(company_allot)

    for i in range(data.shape[0]):
        if(i==0):
            t = 0
        else:
            t = (data['order_pick'][i]-data['order_pick'][i-1]).total_seconds()/60
        
        yield env.timeout(ceil(t))
        c = Customer(env=env, biker=companies[company_allot[i]], name=f'Customer {i+1}', res_long=data['Restaurant_longitude'][i],res_lat=data['Restaurant_latitude'][i], lat=data['Delivery_location_latitude'][i], long=data['Delivery_location_longitude'][i], company=company_allot[i])
        env.process(c.action())





MAX_LAT = max(data['Restaurant_latitude'].max(), data['Delivery_location_latitude'].max())
MIN_LAT = min(data['Restaurant_latitude'].min(), data['Delivery_location_latitude'].min())

MAX_LONG = max(data['Restaurant_longitude'].max(), data['Delivery_location_longitude'].max())
MIN_LONG = min(data['Restaurant_longitude'].min(), data['Delivery_location_longitude'].min())


for i in range(NUM_BOYS):
    BOYS.append({'lat':randrange(10001), 'long':randrange(10001)})

for i in range(NUM_BOYS):
    BOYS[i]['lat'] = MIN_LAT + (MAX_LAT - MIN_LAT)*BOYS[i]['lat']/10000
    BOYS[i]['long'] = MIN_LONG + (MAX_LONG - MIN_LONG)*BOYS[i]['long']/10000
    BOYS[i]['busy'] = 0

class Customer:
    def __init__(self, env, biker, name, res_lat, res_long, lat, long, company):
        self.env = env
        self.biker = biker
        self.name = name
        self.res_lat = res_lat
        self.res_long = res_long
        self.lat = lat
        self.long = long
        self.bike_ind = None
        self.company = company
        self.start_time = 0

    def action(self):
        global NUM_CUSTOMERS
        with self.biker.request() as req:
            NUM_CUSTOMERS += 1
            save_data(self.env.now)
            self.start_time = self.env.now

            # wait for a biker to become free
            yield req

            # find out the nearest biker and wait for him to come to me
            self.bike_ind = get_index_of_nearest_boy(self.res_lat, self.res_long, self.company,self.env.now)
            

            dist1 = man_dist(BOYS[self.bike_ind]['lat'], BOYS[self.bike_ind]['long'], self.res_lat, self.res_long)
            dist2 = man_dist(self.lat, self.long, self.res_lat, self.res_long)

            BOYS[self.bike_ind]['lat'] = self.lat
            BOYS[self.bike_ind]['long'] = self.long

            BOYS[self.bike_ind]['busy'] = self.env.now + ceil(dist1/BIKE_SPEED*60) + ceil(dist2/BIKE_SPEED*60)


            # waiting for nearest biker to go to the restaurant
            yield self.env.timeout(ceil(dist1/BIKE_SPEED*60))

            yield self.env.timeout(ceil(dist2/BIKE_SPEED*60))

            BOYS[self.bike_ind]['busy'] = 0

            NUM_CUSTOMERS -= 1
            save_data(self.env.now)
            ORDER_DATA.append((dist1+dist2, self.env.now-self.start_time))
            



env = simpy.Environment()
companies = []
for i in range(NUM_OF_COMPANIES):
    companies.append(simpy.Resource(env, NUM_BOYS_PER_COMPANY))

env.process(customer_generator(env, companies))

env.run()
# print(f'data = {data}')
# print(f'org_data = {org_data}')






# PLOTTING THE DATA

# for i in customer_resource.data:
x = []
y = []

for i in LOG_DATA:
    # print(i)
    x.append(i[0])
    y.append(i[1])

x = np.array(x)
y = np.array(y)

with open(f"NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_centralised.pkl", 'wb') as file:
    pkl.dump((x,y), file)

with open(f"NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_ORDER_DATA_centralised.pkl", 'wb') as file:
    pkl.dump(ORDER_DATA, file)

plt.plot(x,y)
# plt.bar(x,y)

# plt.plot(x,y, color='blue')
# plt.bar(x,y,color='blue')




NUM_BOYS_PER_COMPANY = 5
NUM_OF_COMPANIES = ceil(NUM_BOYS/NUM_BOYS_PER_COMPANY)




plt.title(f"NUM_BOYS = {NUM_BOYS}, BIKE_SPEED = {BIKE_SPEED}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
plt.xlabel("Time into Simulation")
plt.ylabel("Waiting Queue Length")

plt.show()

