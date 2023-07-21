import pickle as pkl
from pprint import pprint
from collections import Counter

NUM_BOYS_PER_COMPANY = 10 # 4 maybe
NUM_OF_COMPANIES = 20
NUM_BOYS = NUM_BOYS_PER_COMPANY * NUM_OF_COMPANIES # 20 maybe
BIKE_SPEED = 40

K_MEANS_DIST = 2

dataset_acronym = 'ONEDAY'

with open(f"data/{dataset_acronym}_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_K_DIST_{K_MEANS_DIST}_K_MEANS_DATA.pkl", 'rb') as file:
    K_MEANS_DATA = pkl.load(file)

c = Counter()

for i,j in K_MEANS_DATA:
    c[j] += 1

pprint(dict(c))