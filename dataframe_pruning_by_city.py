import pandas as pd
import collections
import pprint
from matplotlib import pyplot as plt

data = pd.read_pickle('data/data_preprocessed.pkl')

MIN_LAT, MAX_LAT, MIN_LONG, MAX_LONG = 16, 20, 71, 73
# for mumbai

city_boundaries = {
    'Mumbai': (16, 20, 71, 73),
    
}


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

print(len(data))

# frequency = collections.Counter(data['Order_Date'])
frequency = collections.Counter(data['order_place'])
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

display_cols = ['order_place', 'order_pick', 'order_delivered']

# pprint.pprint(dict(frequency))
# pprint.pprint(data[display_cols])

# print('-----------------------------------------------------')
# print(data.columns)
data['order_place'].hist(
    bins=36*4
)

# for k in dict(frequency).keys():
#     plt.axvline(x=k, color='#ED4C67', linewidth=1)

# print(dict(frequency).keys())

for i in data.columns:
    print(f'{i}\t{type(data[i])}')

print('-----------------------------------------------------')

print(data['order_place'].iloc[0])
print(type(data['order_place'].iloc[0]))


# plt.show()

# pprint.pprint(data)
# print(len(dict(frequency))) # 36