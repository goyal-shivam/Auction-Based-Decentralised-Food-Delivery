import pandas as pd
import folium

data = pd.read_pickle('data_preprocessed.pkl')
MAX_LAT = max(data['Restaurant_latitude'].max(), data['Delivery_location_latitude'].max())
MIN_LAT = min(data['Restaurant_latitude'].min(), data['Delivery_location_latitude'].min())

MAX_LONG = max(data['Restaurant_longitude'].max(), data['Delivery_location_longitude'].max())
MIN_LONG = min(data['Restaurant_longitude'].min(), data['Delivery_location_longitude'].min())

# print(data.columns)
# 'Restaurant_latitude', 'Restaurant_longitude','Delivery_location_latitude', 'Delivery_location_longitude'
location = set()

for i in range(len(data)):
    location.add((data['Restaurant_latitude'][i], data['Restaurant_longitude'][i]))

# for i in location:
#     folium.Circle(
#         radius=1,
#         location=list(i),
#         color="crimson",
#         fill=False,
#     ).add_to(map)

print(location)

abc = [[13.091809, 80.219104], [11.010375, 76.95295], [21.175104, 72.804342], [12.933284, 77.615428], [21.185047, 72.80859], [-15.157944, 73.950889], [27.160934, 78.044095], [22.74806, 75.8934], [12.323994, 76.626167], [-25.449659, 81.839744], [30.895817, 75.813112], [22.31279, 73.170283], [19.866969, 75.318894], [-19.875908, 75.358888], [30.362686, 78.06889], [30.328174, 78.049117], [18.592718, 73.773572], [23.264015, 77.408236], [23.232537, 77.429845], [18.56245, 73.916619]]

# for i in abc:
#     folium.Circle(
#         radius=1,
#         # location=center,
#         location=i,
#         color="blue",
#         fill=False,
#     ).add_to(map)

center = [(MIN_LAT + MAX_LAT)/2, (MIN_LONG + MAX_LONG)/2]
map = folium.Map(location=center, zoom_start=3)

folium.Circle(
    radius=1,
    location=center,
    color="blue",
    fill=False,
).add_to(map)

for i in abc:
    folium.Marker(
        location=i,
        popup=str(i)
    ).add_to(map)

print(f'Length of abc is {len(abc)}')

map.show_in_browser()