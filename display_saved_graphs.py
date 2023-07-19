from matplotlib import pyplot as plt
import pickle

NUM_BOYS_PER_COMPANY = 1 # 4 maybe
NUM_OF_COMPANIES = 5
NUM_BOYS = NUM_BOYS_PER_COMPANY * NUM_OF_COMPANIES # 20 maybe
BIKE_SPEED = 1 # 25 maybe

# with open('data/mumbai_orders_histogram_shifted.pkl', 'wb') as file:
#     pickle.dump(fig2,file)


''' list of graph file names
data/mumbai_orders_histogram_shifted.pkl
'''

# with open('data/mumbai_orders_histogram_shifted.pkl', 'rb') as file:
#     fig = pickle.load(file)

with open(f"data/graph_queue_length_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
# with open(f"data/graph_queue_length_NUM_BOYS_5_BIKE_SPEED_1__NUM_BOYS_PER_COMPANY_1_NUM_OF_COMPANIES_5.pkl", 'rb') as file:
    # pkl.dump(fig,file)
    fig = pickle.load(file)


'''
with open(f"data/graph_dist_sum_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    # pkl.dump(fig,file)
    fig = pickle.load(file)


with open(f"data/graph_wait_time_sum_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    # pkl.dump(fig,file)
    fig = pickle.load(file)


with open(f"data/graph_dist_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    # pkl.dump(fig,file)
    fig = pickle.load(file)


with open(f"data/graph_wait_time_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'rb') as file:
    # pkl.dump(fig,file)
    fig = pickle.load(file)

'''

plt.show()