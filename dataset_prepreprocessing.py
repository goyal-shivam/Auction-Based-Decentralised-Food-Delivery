import pandas as pd
from datetime import datetime

data = pd.read_csv('data/train.csv')
additional_data = pd.read_excel('data/Additions.xlsx')

data = data.drop(['Delivery_person_ID',
                 'Delivery_person_Age',
                 'Delivery_person_Ratings',
                 'Weatherconditions',
                 'Road_traffic_density',
                 'Vehicle_condition',
                 'Type_of_order',
                 'Type_of_vehicle',
                 'multiple_deliveries',
                 'Festival',
                 'City'], axis=1)

# data['order_pick'] = pd.to_datetime(data['Order_Date']+' '+data['Time_Order_picked'], format="%d-%m-%Y %H:%M:%S", infer_datetime_format=True)

# data['order_place'] = pd.to_datetime(data['Order_Date']+' '+data['Time_Orderd'], format="%d-%m-%Y %H:%M:%S", infer_datetime_format=True)

drop_rows = []
for i in range(len(data)):
    if(data.iat[i,6] == 'NaN '):
        drop_rows.append(i)

data['order_pick'] = '0'
data['order_place'] = '0'
data['order_delivered'] = '0'

# merge the two dataframes here
train_data = data
data = pd.concat([data,additional_data],axis=1)

data = data.drop(drop_rows)

data['order_pick'] = pd.to_datetime(data['Order_Date']+' '+data['Time_Order_picked'], format="%d-%m-%Y %H:%M:%S")

data['order_place'] = pd.to_datetime(data['Order_Date']+' '+data['Time_Orderd'], format="%d-%m-%Y %H:%M:%S")

data['order_delivered'] = data['order_pick'] + pd.Timedelta(minutes=45)

for i in range(len(data)):
    data.iat[i,8] = int(data.iat[i,8].split(' ')[1])

# pd.options.display.max_columns=None
# print(data.head())

pd.to_pickle(data, 'data/data_27_cols.pkl')