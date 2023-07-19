import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
from math import ceil

draw_queue = 1
draw_sums = 1
draw_hists = 1


NUM_BOYS_PER_COMPANY = 3 # 4 maybe
for NUM_BOYS_PER_COMPANY in [3]:
    print(f'############\nNUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}\n#############\n')
    NUM_OF_COMPANIES = 5
    NUM_BOYS = NUM_BOYS_PER_COMPANY * NUM_OF_COMPANIES # 20 maybe
    BIKE_SPEED = 5 # 25 maybe


    # with open('data/mumbai_orders_histogram.pkl', 'rb') as file:
    #     fig2 = pickle.load(file)

    # with open('data/mumbai_orders_histogram_shifted.pkl', 'rb') as file:
    #     fig = pkl.load(file)

    '''
    two queue length colours
    #fc5c65 and #a55eea

    two average line colours
    #20bf6b and #fa8231
    '''


    # PLOT QUEUE LENGTH GRAPH
    if draw_queue > 0:
        with open(f"data/NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}_NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_decent.pkl", 'rb') as file:
            (x,y) = pkl.load(file)

        with open(f"data/NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}_ORDER_DATA.pkl", 'rb') as file:
            ORDER_DATA = pkl.load(file)

        fig = plt.figure(f'Queue Length vs Time_{NUM_BOYS_PER_COMPANY}')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.plot(x,y, color='#fc5c65')

        plt.axhline(np.average(y),0, np.amax(x), color='#20bf6b')
        print(f'\nDecentralised average queue length is {np.average(y)}\n')

        # space for centralised version


        with open(f"data/graph_queue_length_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)


    # PLOT WAIT TIME AND DISTANCE SUM GRAPHS
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

    if (draw_sums > 0):

        plt.figure('Distance Travelled vs Time')
        plt.plot(sum_dist)


        plt.figure('Total wait time vs Time')
        plt.plot(sum_wait)


        # space for centralised version


        plt.figure('Distance Travelled vs Time')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        # plt.plot(sum_dist2)
        plt.xlabel("Number of Orders")
        plt.ylabel("Total Distance travelled by Delivery boys (km)")
        # plt.legend(["Decentralised", "Centralised"])
        plt.legend(["Decentralised"])

        with open(f"data/graph_dist_sum_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)


        plt.figure('Total wait time vs Time')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.xlabel("Number of Orders")
        plt.ylabel("Total Wait time of all customers involved (mins)")
        # plt.plot(sum_wait2)
        # plt.legend(["Decentralised", "Centralised"])
        plt.legend(["Decentralised"])

        with open(f"data/graph_wait_time_sum_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)




    # PLOT WAIT TIME AND DISTANCE HISTOGRAMS
    if (draw_hists>0):
        bins = np.linspace(0, 80, 20)
        bins2 = np.linspace(0, 80, 20)

        plt.style.use('seaborn-deep')
        plt.figure('Distance Histogram')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        # plt.hist([dist, dist2], bins, label=['Decentralised', 'Centralised'])
        plt.hist(dist, bins, label='Decentralised')
        plt.xlabel("Distance (km)")
        plt.ylabel("Frequency")
        plt.legend(loc='upper right')

        with open(f"data/graph_dist_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)

        plt.figure('Wait Time Histogram')
        plt.title(f"NUM_BOYS = {NUM_BOYS}, NUM_BOYS_PER_COMPANY = {NUM_BOYS_PER_COMPANY}, BIKE_SPEED = {BIKE_SPEED}, NUM_OF_COMPANIES = {NUM_OF_COMPANIES}")
        plt.hist(wait, bins2, label='Decentralised')
        plt.xlabel("Wait Time (mins)")
        plt.ylabel("Frequency")
        plt.legend(loc='upper right')

        with open(f"data/graph_wait_time_hist_NUM_BOYS_{NUM_BOYS}_BIKE_SPEED_{BIKE_SPEED}__NUM_BOYS_PER_COMPANY_{NUM_BOYS_PER_COMPANY}_NUM_OF_COMPANIES_{NUM_OF_COMPANIES}.pkl", 'wb') as file:
            pkl.dump(fig,file)



    ''' # PRINTING INFORMATION
    print(f'\nTotal Wait Times\nDecentralised - {sum_wait[-1]} mins and Centralised - {sum_wait2[-1]} mins\n')
    print(f'Total Distance Travelled\nDecentralised - {sum_dist[-1]} kms and Centralised - {sum_dist2[-1]} kms\n')

    print(f'\nAverage Wait Times\nDecentralised - {sum_wait[-1]/len(sum_wait)} mins and Centralised - {sum_wait2[-1]/len(sum_wait2)} mins\n')
    print(f'Average Distance Travelled\nDecentralised - {sum_dist[-1]/len(sum_dist)} kms and Centralised - {sum_dist2[-1]/len(sum_dist2)} kms\n')
    '''

    print(f'\nTotal Wait Times\nDecentralised - {sum_wait[-1]} mins\n')
    print(f'Total Distance Travelled\nDecentralised - {sum_dist[-1]} kms\n')

    print(f'\nAverage Wait Times\nDecentralised - {sum_wait[-1]/len(sum_wait)} mins\n')
    print(f'Average Distance Travelled\nDecentralised - {sum_dist[-1]/len(sum_dist)} kms\n')

    print(f'Max Wait Time = {wait.max()}\nMin Wait Time = {wait.min()}\nMax Distance = {dist.max()}\nMin Distance = {dist.min()}\n')



plt.show()