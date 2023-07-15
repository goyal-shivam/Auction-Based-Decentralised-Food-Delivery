# show the average number of customers waiting at a particular time for both graphs and a legend, in the graph that you have already drawn (DONE!)
# find average of all y values in the graph, and draw a horizontal line

# total distance travelled ka ek figure, cost saved, petrol saved etc.
# distance travelled vs number of orders
# then show total distance travelled
# for each order on it's completion, store the distance travelled and the wait time in a array, and pickle dump this array (DONE!)

# no. of orders delivered per unit time(hour) vs no. of drivers

# average wait time for customer in centralized and decentralized approach
# wait time vs number of orders
# then show average wait time for the customers (DONE!)


# can make a histogram of wait times for the customers

import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
from math import ceil
from matplotlib.transforms import Bbox

NUM_BOYS = 100
BIKE_SPEED = 40
NUM_BOYS_PER_COMPANY = 5
NUM_OF_COMPANIES = ceil(NUM_BOYS/NUM_BOYS_PER_COMPANY)
N_BINS = 20


with open(f"NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_decent.pkl", 'rb') as file:
    (x,y) = pkl.load(file)

with open(f"NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_ORDER_DATA.pkl", 'rb') as file:
    ORDER_DATA = pkl.load(file)

plt.figure('Queue Length vs Time')
plt.plot(x,y, color='#0652DD')
# plt.bar(x,y)

# plt.plot(x,y, color='blue')
# plt.bar(x,y,color='blue')
plt.axhline(np.average(y),0, np.amax(x), color='#12CBC4')

with open(f"NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_centralised.pkl", 'rb') as file:
    (x,y) = pkl.load(file)

plt.plot(x,y, color='#6F1E51')
# plt.bar(x,y)

# plt.plot(x,y, color='blue')
# plt.bar(x,y,color='blue')
plt.axhline(np.average(y),0, np.amax(x), color='#ED4C67')

plt.title(f"NUM_BOYS = {NUM_BOYS}, BIKE_SPEED = {BIKE_SPEED}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
plt.xlabel("Time into Simulation")
plt.ylabel("Waiting Queue Length")

plt.legend(["Decentralised", "Average Decentralised", "Centralised", "Average Centralised"])
plt.savefig("test.svg",format='svg',dpi=300, bbox_inches=Bbox([[0, 0], [100000, 100000]]),pad_inches=1)


dist = []
wait = []

for i in ORDER_DATA:
    dist.append(i[0])
    wait.append(i[1])

dist = np.array(dist)
wait = np.array(wait)
sum_dist = dist.copy()
sum_wait = wait.copy()

for i in range(1,len(ORDER_DATA)):
    sum_dist[i] += sum_dist[i-1]
    sum_wait[i] += sum_wait[i-1]

plt.figure('Distance Travelled vs Time')
plt.plot(sum_dist)


plt.figure('Total wait time vs Time')
plt.plot(sum_wait)

with open(f"NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_ORDER_DATA_centralised.pkl", 'rb') as file:
    ORDER_DATA = pkl.load(file)

dist2 = []
wait2 = []

for i in ORDER_DATA:
    dist2.append(i[0])
    wait2.append(i[1])

dist2 = np.array(dist2)
wait2 = np.array(wait2)
sum_dist2 = dist2.copy()
sum_wait2 = wait2.copy()

for i in range(1,len(ORDER_DATA)):
    sum_dist2[i] += sum_dist2[i-1]
    sum_wait2[i] += sum_wait2[i-1]


plt.figure('Distance Travelled vs Time')
plt.plot(sum_dist2)
plt.xlabel("Number of Orders")
plt.ylabel("Total Distance travelled by Delivery boys")
plt.legend(["Decentralised", "Centralised"])


plt.figure('Total wait time vs Time')
plt.xlabel("Number of Orders")
plt.ylabel("Total Wait time of all customers involved")
plt.plot(sum_wait2)
plt.legend(["Decentralised", "Centralised"])


# fig, axs = plt.subplots()

# axs.hist(x, bins = n_bins,color='r')

# axs.hist(y, bins = n_bins,color='b')

bins = np.linspace(0, 15000, 20)
bins2 = np.linspace(0, 1500, 20)

plt.style.use('seaborn-deep')
plt.figure('Distance Histogram')
plt.hist([dist, dist2], bins, label=['Decentralised', 'Centralised'])
plt.xlabel("Distance")
plt.ylabel("Frequency")
plt.legend(loc='upper right')

plt.figure('Wait Time Histogram')
plt.hist([wait, wait2], bins2, label=['Decentralised', 'Centralised'])
plt.xlabel("Wait Time")
plt.ylabel("Frequency")
plt.legend(loc='upper right')



plt.show()