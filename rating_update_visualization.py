from matplotlib import pyplot as plt
import numpy as np

def update_rider_rating(customer_rating, older_rating, average_rating):

    '''
    hyperparameter
        800 which is present in denominator in sigmoid function
        R_avg or 2500 used in the sigmoid function
        K - 8 or 16 or 32 which is used maximum possible gain/loss in rating per delivery

        P = 1  // if Ri >= threshold for a good rating
        P = 0  // if Ri <= threshold for a bad rating
        threshold used here
    '''    
    e = 1/(1+10**((average_rating-older_rating)/800))

    return older_rating + 32*((1 if customer_rating > 2.5 else 0)-e)


current_rider_rating = 2500
# customer_rating = [3, 1, 5, 4, 1, 2, 3, 2, 5,5,5,1,1,1]
# customer_rating = list(np.linspace(0,5,1000)) + list(np.linspace(5,0,1000))
customer_rating = list(np.linspace(5,0,1000)) + list(np.linspace(0,5,1000))
# customer_rating += list(np.linspace(4.5,5,1000)) + [5]*5000
rating_history = []

for i,j in enumerate(customer_rating):
    current_rider_rating = update_rider_rating(j, current_rider_rating, 2500)
    rating_history.append(current_rider_rating)


print(sum(rating_history)/2000)

plt.plot(customer_rating, color='blue', marker='o', linewidth=2, markersize=6, label='Customer Ratings')
plt.plot(np.array(rating_history)/1000, color='red', marker='x', linewidth=2, markersize=6, label='Rider Rating')
plt.axhline(2.5,0, 5, color='#12CBC4')
plt.axvline(500,0, 5, color='#12CBC4')
plt.axvline(1000,0, 5, color='#12CBC4')
plt.axvline(1500,0, 5, color='#12CBC4')

plt.legend()
plt.show()