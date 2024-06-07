# ALWAYS KEEP THESE LINES
# with open('data/mumbai_orders_histogram_shifted.pkl', 'wb') as file:
#     pickle.dump(fig2,file)

from matplotlib import pyplot as plt
import pickle

NUM_BOYS_PER_COMPANY = 10 # 4 maybe
NUM_OF_COMPANIES = 20
NUM_BOYS = NUM_BOYS_PER_COMPANY * NUM_OF_COMPANIES # 20 maybe
BIKE_SPEED = 40

acronym = 'ONEDAY_'

with open(f"data/graph_queue_length_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    fig = pickle.load(file)
    plt.xlabel("Time (Minutes)", fontsize=16)
    plt.ylabel("Queue Length", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)


with open(f"data/graph_dist_sum_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    fig = pickle.load(file)
    plt.xlabel("Number of Orders", fontsize=16)
    plt.ylabel("Total Distance travelled by Delivery boys (km)", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)


with open(f"data/graph_wait_time_sum_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    fig = pickle.load(file)
    plt.xlabel("Number of Orders", fontsize=16)
    plt.ylabel("Total Wait time of all customers involved (mins)", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)


with open(f"data/graph_dist_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    fig = pickle.load(file)
    plt.xlabel("Distance (km)", fontsize=16)
    plt.ylabel("Frequency", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)


with open(f"data/graph_wait_time_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    fig = pickle.load(file)
    plt.xlabel("Wait Time (mins)", fontsize=16)
    plt.ylabel("Frequency", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)


with open(f"data/{acronym}graph_delivery_charges_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    fig = pickle.load(file)
    plt.xlabel("Delivery Charges (INR)", fontsize=16)
    plt.ylabel("Frequency", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)


with open(f"data/{acronym}graph_customer_rating_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    fig = pickle.load(file)
    plt.xlabel("Customer Ratings for a given order", fontsize=16)
    plt.ylabel("Frequency", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

plt.show()