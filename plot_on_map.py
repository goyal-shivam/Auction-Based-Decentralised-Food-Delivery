import pandas as pd
import folium

data = pd.read_pickle('data_preprocessed.pkl')

MAX_LAT = max(data['Restaurant_latitude'].max(), data['Delivery_location_latitude'].max())
MIN_LAT = min(data['Restaurant_latitude'].min(), data['Delivery_location_latitude'].min())

MAX_LONG = max(data['Restaurant_longitude'].max(), data['Delivery_location_longitude'].max())
MIN_LONG = min(data['Restaurant_longitude'].min(), data['Delivery_location_longitude'].min())

# print(MIN_LAT, MAX_LAT)
# print(MIN_LONG, MAX_LONG)

# print(data.columns)
# 'Restaurant_latitude', 'Restaurant_longitude','Delivery_location_latitude', 'Delivery_location_longitude'

center = [(MIN_LAT + MAX_LAT)/2, (MIN_LONG + MAX_LONG)/2]
map = folium.Map(location=center, zoom_start=3)

# print(dir(map)) # 'render', 'save', 'show_in_browser'
# print(help(map.render))

folium.Circle(
    # radius=100,
    radius=1,
    # location=[45.5244, -122.6699],
    location=center,
    # popup="The Waterfront",
    color="crimson",
    fill=False,
).add_to(map)

map.show_in_browser()