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

'''
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

'''

# ----------------------------------------------------------------------------------------
count = 0
# shifting all orders to 8am to 10pm time
for i in range(len(data)):
    if(
        # data['order_pick'].iloc[i].hour >= 22 or 
        # data.at[i,'Time_taken(min)'] >= 22 or 
        data.iat[i,9].hour >= 22 or 
        # data['order_pick'].iloc[i].hour < 8 or
        data.iat[i,9].hour < 8 or
        # data['order_place'].iloc[i].hour >= 22 or 
        data['order_place'].iloc[i].hour >= 22 or 
        data['order_place'].iloc[i].hour < 8 or
        data['order_delivered'].iloc[i].hour >= 22 or 
        data['order_delivered'].iloc[i].hour < 8
    ):
        # data['order_pick'].iloc[i] += pd.Timedelta(10, 'hours')
        # data.at[i,'order_pick'] += pd.Timedelta(10, 'hours')
        data.iat[i,9] += pd.Timedelta(10, 'hours')
        data['order_place'].iloc[i] += pd.Timedelta(10, 'hours')
        data['order_delivered'].iloc[i] += pd.Timedelta(10, 'hours')

        count += 1
        if(count >=10):
            break


pd.options.display.max_columns = None
pd.options.display.max_rows = None
# pprint(data[['order_pick', 'order_place', 'order_delivered']])


# '''
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


with open('mumbai_orders_histogram_shifted.pkl', 'wb') as file:
    pickle.dump(fig2,file)





# '''
# ----------------------------------------------------------------------------------------
plt.show()