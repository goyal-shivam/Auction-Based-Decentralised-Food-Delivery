import pandas as pd
import collections
from pprint import pprint
from matplotlib import pyplot as plt
import pickle

data = pd.read_pickle('data/data_preprocessed.pkl')

MIN_LAT, MAX_LAT, MIN_LONG, MAX_LONG = 16, 20, 71, 73
# for mumbai

data = data[
            (data['Restaurant_latitude'] <= MAX_LAT) &
            (data['Restaurant_latitude'] >= MIN_LAT) &
            (data['Restaurant_longitude'] <= MAX_LONG) &
            (data['Restaurant_longitude'] >= MIN_LONG) &
            (data['Delivery_location_latitude'] <= MAX_LAT) &
            (data['Delivery_location_latitude'] >= MIN_LAT) &
            (data['Delivery_location_longitude'] <= MAX_LONG) &
            (data['Delivery_location_longitude'] >= MIN_LONG)
        ]

date_set = set()
green_date_set = set()

for i in range(len(data)):
    date_set.add(
        data['order_place'].iloc[i].replace(
            hour=0,
            minute=0,
            second=0
        )
    )

    green_date_set.add(data['order_place'].iloc[i].replace(
            hour=6, minute=0, second=0))
    green_date_set.add(data['order_place'].iloc[i].replace(
            hour=12, minute=0, second=0))
    green_date_set.add(data['order_place'].iloc[i].replace(
            hour=18, minute=0, second=0))

fig = plt.figure('Histogram showing frequency of orders in Mumbai every 6 hours')
plt.xlabel("Date (divided in 6hr slots)")
plt.ylabel("Number of orders")

data['order_place'].hist(
    bins=sorted(list(date_set.union(green_date_set)))
)

for k in date_set:
    plt.axvline(x=k, color='#ED4C67', linewidth=1)
for k in green_date_set:
    plt.axvline(x=k, color='#55A868', linewidth=1)


with open('mumbai_orders_histogram.pkl', 'wb') as file:
    pickle.dump(fig,file)

plt.show()