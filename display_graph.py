from matplotlib import pyplot as plt
import pickle

with open('mumbai_orders_histogram.pkl', 'rb') as file:
    fig2 = pickle.load(file)

plt.show()