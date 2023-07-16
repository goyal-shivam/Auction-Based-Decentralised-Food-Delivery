import pandas as pd
import folium

data = pd.read_pickle('data_preprocessed.pkl')
MAX_LAT = max(data['Restaurant_latitude'].max(), data['Delivery_location_latitude'].max())
MIN_LAT = min(data['Restaurant_latitude'].min(), data['Delivery_location_latitude'].min())
MAX_LONG = max(data['Restaurant_longitude'].max(), data['Delivery_location_longitude'].max())
MIN_LONG = min(data['Restaurant_longitude'].min(), data['Delivery_location_longitude'].min())
center = [(MIN_LAT + MAX_LAT)/2, (MIN_LONG + MAX_LONG)/2]

location = set()
people = set()

for i in range(len(data)):
    location.add((data['Restaurant_latitude'][i], data['Restaurant_longitude'][i]))

for i in range(len(data)):
    people.add((data['Delivery_location_latitude'][i], data['Delivery_location_longitude'][i]))

center = (19.091458, 72.827808)
map = folium.Map(location=center, zoom_start=12)
# map = folium.Map(location=center, zoom_start=1)

# Plot restaurants with red marker on the map
for i in location:
    x = list(i)
    folium.Marker(
        location=i,
        popup=str(i),
        # icon=folium.Icon(color="green")
        icon=folium.Icon(color="red", icon="glyphicon-remove-circle")
    ).add_to(map)

# Plot client locations with blue marker on the map
for i in people:
    x = list(i)
    folium.Marker(
        location=i,
        popup=str(i),
        # icon=folium.Icon(color="green")
        icon=folium.Icon(color="blue")
    ).add_to(map)



map.show_in_browser()