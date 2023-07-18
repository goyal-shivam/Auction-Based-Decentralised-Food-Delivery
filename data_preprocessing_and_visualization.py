'''
NOTES - 
    Just use the order_place column of this dataset, other columns are not to be used. Only order_place column has been corrected from the original dataset
'''

import pandas as pd
from pprint import pprint
from matplotlib import pyplot as plt
import pickle
from collections import Counter

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

# ------------------------------------------------------------------------------------

# shifting all orders to 8am to 10pm time
for i in range(len(data)):
    if(
        data.iat[i,10].hour >= 21 or 
        data.iat[i,10].hour < 8
    ):
        data.iat[i,10] += pd.Timedelta(11, 'hours')

# shifting all order dates to 1 to 7th April
for i in range(len(data)):
    data.iat[i,10] = data.iat[i,10].replace(
        day=(data.iat[i,10].day % 7)+1,
        month=4
    )

date_set = set()
green_date_set = set()
purple_date_set = set()

for i in range(len(data)):
    date_set.add(
        data.iat[i,10].replace(
            hour=0,
            minute=0,
            second=0
        )
    )

    # green_date_set.add(data.iat[i,10].replace(
    #         hour=6, minute=0, second=0))
    # green_date_set.add(data.iat[i,10].replace(
    #         hour=12, minute=0, second=0))
    # green_date_set.add(data.iat[i,10].replace(
    #         hour=18, minute=0, second=0))

    for j in range(1,24):
        green_date_set.add(data.iat[i,10].replace(
            hour=j, minute=0, second=0))
        
    for j in [6,12,18]:
        purple_date_set.add(data.iat[i,10].replace(
            hour=j, minute=0, second=0))



fig2 = plt.figure('Mumbai orders Histogram shifted to 8am-10pm slot')
plt.xlabel("Date (divided in 6hr slots)")
plt.ylabel("Number of orders")

data['order_place'].hist(
    bins=sorted(list(date_set.union(green_date_set)))
)

for k in date_set:
    plt.axvline(x=k, color='#ED4C67', linewidth=1)
for k in green_date_set:
    plt.axvline(x=k, color='#55A868', linewidth=1)
for k in purple_date_set:
    plt.axvline(x=k, color='#8e44ad', linewidth=1)


with open('data/mumbai_orders_histogram_shifted.pkl', 'wb') as file:
    pickle.dump(fig2,file)


# ----------------------------------------------------------------------------------------


c = Counter()

for i in range(len(data)):
    c[data.iat[i,10].date()] += 1

pprint(dict(c))
print(len(dict(c)))

data.sort_values('order_place', inplace=True)

data.to_pickle('data/mumbai_7_days_data.pkl')


plt.show()
