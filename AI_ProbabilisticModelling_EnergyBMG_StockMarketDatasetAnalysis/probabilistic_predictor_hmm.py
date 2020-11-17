# Loading historical stock quotes from matplotlib package for this example code. Work done with pre-defined data for multiple portfolios.

import datetime
import warnings

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ochl\
        as quotes_yahoo
from hmmlearn.hmm import GaussianHMM

start = datetime.date(1970, 7, 3) 
end = datetime.date(2016, 9, 18)
stock_quote = quotes_yahoo('INTC', start, end) 

closing_quote = np.array([quote[2] for quote in stock_quote])

volume = np.array([quote[5] for quote in stock_quote])[1:]

diff_percentage = 100.0 * np.diff(closing_quote) / closing_quote[:-1]

date = np.array([quote[0] for quote in stock_quote], dtype=np.int)[1:]

train_data = np.column_stack([diff_percentage, volume])

# Creating and training a Gaussian HMM Model 
hmm = GaussianHMM(n_components=7, covariance_type='diag', n_iter=1000)
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    hmm.fit(train_data)

# Generating data using the HMM model
num_sample = 900 
samples, _ = hmm.sample(num_sample) 

plt.figure()
plt.title('Difference in percentage of Closing Quotes')
plt.plot(np.arange(num_sample), samples[:, 0], c='black')

plt.figure()
plt.title('Volume of shares traded')
plt.plot(np.arange(num_sample), samples[:, 1], c='black')
plt.ylim(ymin=0)

plt.show()

