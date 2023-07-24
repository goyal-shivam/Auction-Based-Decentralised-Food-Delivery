from matplotlib import pyplot as plt
import pandas as pd
import pickle as pkl
import numpy as np

def min_bid (order):
    return order * 0.1

def max_bid (order):
    return order * 0.2

def machine_predicted_bid(filename):
    data = pd.read_pickle(filename)
    order = data['order_cost']
    data['update'] = 10 * data['Time_taken(min)']
        
    # normal_update = np.empty((len(data), 1), dtype = float)
    
    m = max(data['update'])
    n = min(data['update'])
    
    data['normal_update'] = (m - data['update']) * 5 / (m - n)
                         
    id = np.empty((len(data), 1), dtype = int)
    
    for i in range(0, len(id)):
        id[i] = i + 1
    
    data['ID'] = id

    p = data['Weight_1'] * data['Order_1'] + data['Weight_2'] * data['Order_2'] + data['Weight_3'] * data['Order_3'] + data['WeightA_1'] * data['Active_1'] + data['WeightA_2'] * data['Active_2'] + data['WeightA_3'] * data['Active_3']
    
    # Finding factor a
    a = data['order_history_weight'] * p + data['rating_weight'] * data['normal_update']
    
    data['update'] = data['update'] + (a / 100000)
    
    # Updated Ratings of the rider
    data['updated_ratings'] = data['Delivery_person_Ratings'] + (data['normal_update'] / 10)
    sample_size = 15
    
    # Sampling without replacement
    sample = data.sample(n = sample_size)
    
    id = np.empty((sample_size, 1), dtype = int)
    
    for i in range(0, len(id)):
        id[i] = i + 1
    
    sample['id'] = id
    
    # bid = np.empty((len(data), 1), dtype = float)
    pd.to_pickle(data,'data/uday_stats_mumbai_data.pkl')
    exp_array = data['updated_ratings'].to_numpy(dtype=float,copy=True)
    # x = 1 / (1 + np.exp(np.ndarray(-data['updated_ratings'].values)))
    x = 1 / (1 + np.exp(exp_array))
    x = (x - 0.5) / 0.5
    data['bid'] = x * (max_bid(order) - min_bid(order)) + min_bid(order)
    
    data['bid'] = data['bid'] / max(data['bid'])
    data['bid'] = data['bid'] * max_bid(order)
    
    data['machine_bid'] = data['bid']
    
    sample_size = len(data)
    sample = data.sample(n = sample_size)

    # change refers to the change in the rating of the rider

    id = np.empty((sample_size, 1), dtype = int)
    
    for i in range(0, len(id)):
        id[i] = i + 1
    
    sample['id'] = id
    sample['change'] = sample['updated_ratings'] - sample['Delivery_person_Ratings']
    sample = sample.sort_values(by = ['change'])

    # return data['bid']
    return data

result = machine_predicted_bid('data/mumbai_all_in_one_day.pkl')
# machine_predicted_bid('mumbai_7_days_data.pkl')


result['bid'].hist(
    bins=10
)

plt.figure()

result['order_cost'].hist()

plt.show()