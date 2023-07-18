from matplotlib import pyplot as plt
import pickle

# with open('data/mumbai_orders_histogram.pkl', 'rb') as file:
#     fig2 = pickle.load(file)

with open('data/mumbai_orders_histogram_shifted.pkl', 'rb') as file:
    fig = pickle.load(file)
plt.show()