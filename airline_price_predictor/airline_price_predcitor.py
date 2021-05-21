import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import ExtraTreesRegressor

sns.set()

train_data = pd.read_excel('archive/Data_Train.xlsx')

# Since the computer or the model does not understand the hours, minutes
# and days, we used the pd.to_datetime to convert these values into values
# that can be understood by the computer

train_data["Journey_day"] = pd.to_datetime(train_data.Date_of_Journey, format = "%d/%m/%Y").dt.day
train_data["Journey_month"] = pd.to_datetime(train_data['Date_of_Journey'], format = "%d/%m/%Y").dt.month
train_data.drop(['Date_of_Journey'], axis = 1, inplace = True)

train_data["Dep_hour"] = pd.to_datetime(train_data['Dep_Time']).dt.hour
train_data['Dep_min'] = pd.to_datetime(train_data['Dep_Time']).dt.minute
train_data.drop(["Dep_Time"],axis = 1, inplace = True)

train_data['Arrival_hour'] = pd.to_datetime(train_data.Arrival_Time).dt.hour
train_data['Arrival_minute'] = pd.to_datetime(train_data.Arrival_Time).dt.minute
train_data.drop(['Arrival_Time'], axis = 1, inplace = True)

# The duration of the flight is in hours and minutes which again the computer cannot
# understand

duration = list(train_data['Duration'])

for i in range(len(duration)):
    if len(duration[i].split()) != 2:
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"
        else:
            duration[i] = "0h" + duration[i]

duration_hours = []
duration_mins = []

for i in range(len(duration)):
    duration_hours.append(int(duration[i].split(sep = "h")[0]))
    duration_mins.append(duration[i].split(sep = "m")[0].split()[-1])

train_data['Duration_hours'] = duration_hours
train_data['Duration_mins'] = duration_mins

train_data.drop(['Duration'],axis = 1, inplace = True)

# Using OneHotEncoder for ordinal data which means that the data is in
# order

sns.catplot(y = "Price", x = "Airline", data = train_data.sort_values("Price", ascending = False), kind="boxen", height = 6, aspect = 3)
# print(plt.show())

Airline = train_data[["Airline"]]
Airline = pd.get_dummies(Airline , drop_first=True)


# Source vs price
sns.catplot(y = "Price", x = "Source", data = train_data.sort_values('Price'), kind="boxen", height = 6, aspect = 3)
# plt.show()

# As source is also a nominal catgorlcal data will perform OneHotEncoding
Source = train_data[["Source"]]

Source = pd.get_dummies(Source, drop_first = True)

train_data['Destination'].value_counts()

train_data.drop(["Route", "Additional_Info"], axis = 1, inplace = True)

train_data.replace({"non-stop" : 0, "1 stop": 1, "2 stops" : 2, "3 stops" : 3, "4 stops" : 4}, inplace = True)

Destination = train_data[['Destination']]
Destination = pd.get_dummies(Destination, drop_first = True)

data_train = pd.concat([train_data, Airline, Source, Destination], axis = 1)

data_train.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)
data_train.head()

test_data = pd.read_excel(r'archive/Test_set.xlsx')
# print(test_data.head())

# Steps for preprocessing
# print('Test data info')
# print("-" * 75)
# print(test_data.info())

print()
print()

#print("Null values :")
#print("-" * 75)
test_data.dropna(inplace = True)
#print(test_data.isnull().sum())

# Date of journey
test_data["Journey_day"] = pd.to_datetime(test_data.Date_of_Journey, format = "%d/%m/%Y").dt.day
test_data["Journey_moth"] = pd.to_datetime(test_data["Date_of_Journey"], format = "%d/%m/%Y").dt.month
test_data.drop(["Date_of_Journey"], axis = 1, inplace = True)

# Dep time
test_data['Dep_hour'] = pd.to_datetime(test_data['Dep_Time']).dt.hour
test_data['Dep_min'] = pd.to_datetime(test_data['Dep_Time']).dt.minute
test_data.drop(['Dep_Time'], axis = 1, inplace = True)

# Arrival Time
test_data['Arrival_hour'] = pd.to_datetime(test_data.Arrival_Time).dt.hour
test_data['Arrival_min'] = pd.to_datetime(test_data.Arrival_Time).dt.minute

# Duration
duration = list(test_data['Duration'])

for i in range(len(duration)):
    if len(duration[i].split()) != 2:
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"
        else:
            duration[i] = " 0h" + duration[i]


duration_hours = []
duration_mins = []

for i in range(len(duration)):
    duration_hours.append(int(duration[i].split(sep = "h")[0]))
    duration_mins.append(duration[i].split(sep = "m")[0].split()[-1])

test_data['Duration_hours'] = duration_hours
test_data['Duration_mins'] = duration_mins

test_data.drop(['Duration'], axis = 1, inplace = True)

# Airline
Airline = test_data[["Airline"]]
Airline = pd.get_dummies(Airline , drop_first=True)

 # Source
Source = test_data[["Source"]]

Source = pd.get_dummies(Source, drop_first = True)

test_data['Destination'].value_counts()

test_data.drop(["Route", "Additional_Info"], axis = 1, inplace = True)

test_data.replace({"non-stop" : 0, "1 stop": 1, "2 stops" : 2, "3 stops" : 3, "4 stops" : 4}, inplace = True)

Destination = test_data[['Destination']]
Destination = pd.get_dummies(Destination, drop_first = True)

data_test = pd.concat([test_data, Airline, Source, Destination], axis = 1)

data_test.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)

# Feature Scaling
X = data_train.loc[:, ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
       'Dep_min', 'Arrival_hour', 'Arrival_minute', 'Duration_hours',
       'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
       'Airline_Jet Airways', 'Airline_Jet Airways Business',
       'Airline_Multiple carriers',
       'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
       'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
       'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
       'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
       'Destination_Kolkata', 'Destination_New Delhi']]

y = data_train.iloc[:, 1]

plt.figure(figsize = (18, 18))
sns.heatmap(train_data.corr(), annot=True, cmap = "RdYlGn")

print(X.head())
print(y.head())

selection = ExtraTreesRegressor()
selection.fit(X, y)
print(selection.feature_importances_)

plt.figure(figsize=(12, 8))


feat_importances = pd.Series(selection.feature_importances_, index = X.columns)
feat_importances.nlargest(20).plot(kind = "barh")
plt.show()

