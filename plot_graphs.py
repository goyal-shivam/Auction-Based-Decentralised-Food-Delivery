import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
from math import ceil
import pandas as pd

draw_queue = 1
draw_sums = 1
draw_hists = 1
res, res2 = None, None

'''
two queue length colours
#fc5c65 and #a55eea
two average line colours
#576574 and #222f3e
# 20bf6b and #fa8231 not so good
'''
queue_length_colour = ('#fc5c65', '#a55eea')
average_line_colours = ('#10ac84', '#222f3e')
acronym = 'ONEDAY_'

'''
NUM_BOYS_PER_COMPANY = 2 # 4 maybe
'''
for NUM_BOYS_PER_COMPANY in [10]:
    NUM_OF_COMPANIES = 20
    NUM_BOYS = NUM_BOYS_PER_COMPANY * NUM_OF_COMPANIES # 20 maybe
    BIKE_SPEED = 40
    print(f"NUM_BOYS = {NUM_BOYS}\nBIKE_SPEED = {BIKE_SPEED}\nNUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}\nNUM_OF_COMPANIES = {NUM_OF_COMPANIES}\n\n")


    # PLOT QUEUE LENGTH GRAPH
    if draw_queue > 0:
        with open(f"data/{acronym}NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_decent.pkl", 'rb') as file:
            (x,y) = pkl.load(file)

        fig = plt.figure(f'Queue Length vs Time')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.plot(x,y, color=queue_length_colour[0])
        plt.xlabel("Time into Simulation")
        plt.ylabel("Waiting Queue Length")

        res = np.average(y)
        plt.axhline(np.average(y),0, np.amax(x), color=average_line_colours[0])

        # SPACE FOR CENTRALISED VERSION
        with open(f"data/{acronym}NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_centralised.pkl", 'rb') as file:
            (x,y) = pkl.load(file)

        fig = plt.figure(f'Queue Length vs Time')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.plot(x,y, color=queue_length_colour[1])

        plt.axhline(np.average(y),0, np.amax(x), color=average_line_colours[1])
        res2 = np.average(y)

        plt.legend(["Decentralised", "Average Decentralised", "Centralised", "Average Centralised"])

        # saving graph
        with open(f"data/{acronym}graph_queue_length_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)


    # PLOT WAIT TIME AND DISTANCE SUM GRAPHS

    with open(f"data/{acronym}NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_ORDER_DATA.pkl", 'rb') as file:
            ORDER_DATA = pkl.load(file)

    dist = []
    wait = []

    for i in ORDER_DATA:
        dist.append(i[0])
        wait.append(i[1])

    dist = np.array(dist)
    wait = np.array(wait)
    sum_dist = dist.copy()
    sum_wait = wait.copy()

    for i in range(1,len(ORDER_DATA)):
        sum_dist[i] += sum_dist[i-1]
        sum_wait[i] += sum_wait[i-1]


    with open(f"data/{acronym}NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_ORDER_DATA_centralised.pkl", 'rb') as file:
        ORDER_DATA = pkl.load(file)


    dist2 = []
    wait2 = []

    for i in ORDER_DATA:
        dist2.append(i[0])
        wait2.append(i[1])

    dist2 = np.array(dist2)
    wait2 = np.array(wait2)
    sum_dist2 = dist2.copy()
    sum_wait2 = wait2.copy()

    for i in range(1,len(ORDER_DATA)):
        sum_dist2[i] += sum_dist2[i-1]
        sum_wait2[i] += sum_wait2[i-1]

    if (draw_sums > 0):

        plt.figure('Distance Travelled vs Time')
        plt.plot(sum_dist)


        plt.figure('Total wait time vs Time')
        plt.plot(sum_wait)


        # SPACE FOR CENTRALISED VERSION

        fig = plt.figure('Distance Travelled vs Time')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.plot(sum_dist2)
        plt.xlabel("Number of Orders")
        plt.ylabel("Total Distance travelled by Delivery boys (km)")
        plt.legend(["Decentralised", "Centralised"])

        with open(f"data/{acronym}graph_dist_sum_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)


        fig = plt.figure('Total wait time vs Time')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.xlabel("Number of Orders")
        plt.ylabel("Total Wait time of all customers involved (mins)")
        plt.plot(sum_wait2)
        plt.legend(["Decentralised", "Centralised"])

        with open(f"data/{acronym}graph_wait_time_sum_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)




    # PLOT WAIT TIME AND DISTANCE HISTOGRAMS
    if (draw_hists>0):
        bins = list(range(0,int(max(dist.max(),dist2.max())),5))
        bins = np.array(bins)
        bins2 = list(range(0,int(max(wait.max(),wait2.max())),5))
        bins2 = np.array(bins2)
        # bins = np.linspace(0, max(dist.max(),dist2.max()), 20)
        # bins2 = np.linspace(0, max(wait.max(), wait2.max()), 20)

        plt.style.use('seaborn-deep')
        fig = plt.figure('Distance Histogram')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.hist([dist, dist2], bins, label=['Decentralised', 'Centralised'])
        plt.xlabel("Distance (km)")
        plt.ylabel("Frequency")
        plt.legend(loc='upper right')

        with open(f"data/{acronym}graph_dist_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)

        fig = plt.figure('Wait Time Histogram')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.hist([wait, wait2], bins2, label=['Decentralised', 'Centralised'])
        plt.xlabel("Wait Time (mins)")
        plt.ylabel("Frequency")
        plt.legend(loc='upper right')

        with open(f"data/{acronym}graph_wait_time_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)



# mean, min, max, median, sum
    arrays = [
        np.array(["Distance", "Distance", "Distance", "Distance", "Distance", "Wait Time", "Wait Time", "Wait Time", "Wait Time", "Wait Time", 'Average']),
        np.array(["Min", "Median", "Max", "Sum", "Average", "Min", "Median", "Max", "Sum", "Average", 'Queue Length'])
    ]

    results = [
        [np.min(dist),np.min(dist2)],
        [np.median(dist),np.median(dist2)],
        [np.max(dist),np.max(dist2)],
        [np.sum(dist),np.sum(dist2)],
        [np.average(dist),np.average(dist2)],
        [np.min(wait),np.min(wait2)],
        [np.median(wait),np.median(wait2)],
        [np.max(wait),np.max(wait2)],
        [np.sum(wait),np.sum(wait2)],
        [np.average(wait),np.average(wait2)],
        [res,res2]
    ]

    results = pd.DataFrame(results, index=arrays)
    results.columns = ['Decentralised', 'Centralised']
    results['Improvement'] = (results['Decentralised']/results['Centralised'])*100
    print(results)



plt.show()