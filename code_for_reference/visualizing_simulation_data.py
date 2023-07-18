# code_for_reference/NUM_BOYS_100_BIKE_SPEED_40_decent.pkl

import pickle as pkl
import os

with open(f"code_for_reference/NUM_BOYS_100_BIKE_SPEED_40_decent.pkl", 'rb') as file:
    (x,y) = pkl.load(file)

# print(type(x))
# print(type(y))
# print(os.listdir('.'))
