#New Delhi Traffic data used to predict traffic concentration 
#Results used to suggest efficient energy usage, causing minimal pollution.
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, mean_absolute_error
from sklearn import cross_validation, preprocessing
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import classification_report

input_file = 'newdelhi_traffic_data.txt'
data = []
with open(input_file, 'r') as f:
    for line in f.readlines():
        comps = line[:-1].split(',')
        data.append(comps)

data = np.array(data)

# Converting string data to numerical data and assigning labels
label_encode = [] 
X_encode = np.empty(data.shape)
for i, item in enumerate(data[0]):
    if item.isdigit():
        X_encode[:, i] = data[:, i]
    else:
        label_encode.append(preprocessing.LabelEncoder())
        X_encode[:, i] = label_encode[-1].fit_transform(data[:, i])

X = X_encode[:, :-1].astype(int)
y = X_encode[:, -1].astype(int)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        X, y, test_size=0.25, random_state=5)

# Extremely Random Forests Regressor
parameters = {'n_estimators': 100, 'max_depth': 4, 'random_state': 0}
erfr = ExtraTreesRegressor(**parameters)
erfr.fit(X_train, y_train)

# Compute the regressor performance on test data
y_pred = erfr.predict(X_test)
print("Mean Absolute Error:", round(mean_absolute_error(y_test, y_pred), 2))

# Testing encoding on single data instance
test_datapt = ['Saturday', '10:20', 'Connaught Place', 'no']
test_datapt_encode = [-1] * len(test_datapt)
cnt = 0
for i, item in enumerate(test_datapt):
    if item.isdigit():
        test_datapt_encode[i] = int(test_datapt[i])
    else:
        test_datapt_encode[i] = int(label_encode[count].transform(test_datapt[i]))
        cnt = cnt + 1 

test_datapt_encode = np.array(test_datapt_encode)

# Predicting the output for the test datapoint
print("Predicted traffic:", int(erfr.predict([test_datapt_encode])[0]))

