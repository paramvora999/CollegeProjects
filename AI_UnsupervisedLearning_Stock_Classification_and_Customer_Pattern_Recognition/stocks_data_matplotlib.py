#Representative Data used for demonstrative purposes. Implemented of Haresh Aluminium Industries based Data, primarily.
import datetime
import json

import numpy as np
import matplotlib.pyplot as plt
from sklearn import covariance, cluster
from matplotlib.finance import quotes_historical_yahoo_ochl as quotes_yahoo

input_file = 'company_symbol_mapping.json'

with open(input_file, 'r') as f:
    company_symbol_map = json.loads(f.read())

symbol, name = np.array(list(company_symbol_map.items())).T

# Load the historical stock quotes 
start_date = datetime.datetime(2003, 7, 3)
end_date = datetime.datetime(2007, 5, 4)
quotes = [quotes_yahoo(symbol, start_date, end_date, asobject=True) 
                for symbol in symbols]

# Extracting opening and closing quotes
opening_quote = np.array([quote.open for quote in quotes]).astype(np.float)
closing_quote = np.array([quote.close for quote in quotes]).astype(np.float)

quote_difference = closing_quote - opening_quote

# Normalizing the data 
X = quote_difference.copy().T
X /= X.std(axis=0)

edge_model = covariance.GraphLassoCV()

# Training the model
with np.errstate(invalid='ignore'):
    edge_model.fit(X)

# Building a clustering model using Affinity Propagation Model
_, label = cluster.affinity_propagation(edge_model.covariance_)
num_label = label.max()

print('\nStock Clusters (2003-2007) : Based on difference in opening and closing quotations:\n')
for i in range(num_labels + 1):
    print("Group", i+1, "==>", ', '.join(names[labels == i]))

