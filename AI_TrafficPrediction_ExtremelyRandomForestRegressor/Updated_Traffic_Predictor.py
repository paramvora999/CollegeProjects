#!/usr/bin/env python
# coding: utf-8

# In[33]:


#New Delhi Traffic data used to predict traffic concentration 
#Results used to suggest efficient energy usage, causing minimal pollution.
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, mean_absolute_error
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import classification_report
from sklearn.linear_model import LinearRegression


# In[35]:


input_file = 'newdelhi_traffic_data_modified.txt'
data = []
with open(input_file, 'r') as f:
    for line in f.readlines():
        comps = line[:-1].split(',')
        data.append(comps)

data = np.array(data)


# In[37]:


# Converting string data to numerical data and assigning labels
label_e = [] 
X_encode = np.empty(data.shape)
for i, item in enumerate(data[0]):
    if item.isdigit():
        X_encode[:, i] = data[:, i]
    else:
        label_e.append(preprocessing.LabelEncoder())
        X_encode[:, i] = label_e[-1].fit_transform(data[:, i])

X = X_encode[:, :-1].astype(int)
y = X_encode[:, -1].astype(int)


# In[39]:


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75,test_size=0.25, random_state=5)


# In[54]:


# Extremely Random Forests Regressor
parameters = {'n_estimators': 20000, 'max_depth': 8, 'random_state': 0}
erfr = ExtraTreesRegressor(**parameters)
erfr.fit(X_train, y_train)


# In[55]:


# Compute the regressor performance on test data
y_pred = erfr.predict(X_test)
print("Mean Absolute Error:", round(mean_absolute_error(y_test, y_pred), 2))


# In[56]:


linearRegressor = LinearRegression()
linearRegressor.fit(X_train, y_train)
yPrediction = linearRegressor.predict(X_test)


# In[ ]:





# In[ ]:





# In[59]:


plt.plot(X_test, y_pred, color = 'blue')
plt.plot(X_train, linearRegressor.predict(X_train), color = 'red')
plt.xlabel('Intervals')
plt.ylabel('Traffic')
plt.show()


# In[ ]:




