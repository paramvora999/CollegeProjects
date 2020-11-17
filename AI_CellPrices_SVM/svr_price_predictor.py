import numpy as np
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, explained_variance_score
from sklearn.utils import shuffle
import pandas as pd

data =  pd.read_csv('pvcell_prices_kol.csv')

X, y = shuffle(data.data, data.target, random_state=7)

# Splitting the data into training and testing datasets 
num_training = int(0.8 * len(X))
X_train, y_train = X[:num_training], y[:num_training]
X_test, y_test = X[num_training:], y[num_training:]

# Creating Support Vector Regression model
svr = SVR(kernel='linear', C=1.0, epsilon=0.1)

svr.fit(X_train, y_train)

y_test_pred = svr.predict(X_test)
mse = mean_squared_error(y_test, y_test_pred)
evs = explained_variance_score(y_test, y_test_pred) 
print("\nResult\n")
print("Mean squared error =", round(mse, 3))
print("Explained Variance Score =", round(evs, 3))

print("\nPredicted Price:", svr.predict(y_test))

