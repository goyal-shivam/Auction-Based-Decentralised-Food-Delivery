from matplotlib import pyplot as plt
import pickle

# with open('data/mumbai_orders_histogram_shifted.pkl', 'wb') as file:
#     pickle.dump(fig2,file)

''' list of graph file names
data/mumbai_orders_histogram_shifted.pkl
'''

with open('data/mumbai_orders_histogram_shifted.pkl', 'rb') as file:
    fig = pickle.load(file)
plt.show()