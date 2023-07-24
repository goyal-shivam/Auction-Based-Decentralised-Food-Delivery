from matplotlib import pyplot as plt
import numpy as np

def update_rider_rating(customer_rating, older_rating, num_rides):
    # create global variable to store min and max wait time
    # older_rating = rider_data['rating']

    # k = np.exp(-num_rides)
    k = 0.01
    
    rating_update = 0.2*np.exp(k*(abs(customer_rating-older_rating) - 5))

    return older_rating + np.sign(customer_rating-older_rating)*(rating_update) # we want maximum 0.1 change in rating, so we multiply by 0.02, so that even when difference in rating is 5, the final increment/decrement in rating is less than 0.1 only

current_rider_rating = 3
customer_rating = [3, 1, 5, 4, 1, 2, 3, 2, 5,5,5,1,1,1]
rating_history = []

for i,j in enumerate(customer_rating):
    current_rider_rating = update_rider_rating(j, current_rider_rating, i+1)
    rating_history.append(current_rider_rating)
    # print(i,j)

# plt.plot(customer_rating, 'bo')
plt.plot(rating_history, 'r+')

# plt.plot(customer_rating, color='blue', marker='o', linestyle='dashed',linewidth=2, markersize=6)
plt.plot(customer_rating, color='blue', marker='o', linewidth=2, markersize=6)
plt.plot(rating_history, color='red', marker='x', linewidth=2, markersize=6)
plt.legend(['Customer Ratings', 'Rider Rating'])
plt.show()