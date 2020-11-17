import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


appl = pd.read_csv('appl_CLOSE',index_col='Date',parse_dates=True)
cisco = pd.read_csv('CISCO_CLOSE',index_col='Date',parse_dates=True)
ibm = pd.read_csv('IBM_CLOSE',index_col='Date',parse_dates=True)
amazn = pd.read_csv('amazn_CLOSE',index_col='Date',parse_dates=True)

stock = pd.concat([appl,cisco,ibm,amazn],axis=1)
stock.columns = ['appl','cisco','ibm','amazn']

stock.head()

mean_daily_returnsurn = stock.pct_change(1).mean()

stock.pct_change(1).corr()
stock.head()

stock_normalize = stock/stock.iloc[0]
stock_normalize.plot()

stock_daily_returns = stock.pct_change(1)
stock_daily_returns.head()

log_val_returns = np.log(stock/stock.shift(1))
log_val_returns.head()

log_val_returns.hist(bins=100,figsize=(12,6));
plt.tight_layout()

log_val_returns.mean() * 252
log_val_returns.cov()
log_val_returns.cov()*252 

np.random.seed(101)

print('Stock Valuations on given Exchange :')
print(stock.columns)
print('\n')

print('Creating Random Weight for Monte Carlo Simulation.')
weight = np.array(np.random.random(4))
print(weight)
print('\n')

weight = weight / np.sum(weight)
print(weight)
print('\n')

print('Expected Portfolio-wise Returns Analysis :')
exp_returns = np.sum(log_val_returnsurn.mean() * weight) *252
print(exp_returns)
print('\n')

SR = exp_returns/exp_volumes
print('Sharpe Ratio for each Portfolio :')
print(SR)

num_ports = 15000

all_weight = np.zeros((num_ports,len(stock.columns)))
returns_arr = np.zeros(num_ports)
volumes_arr = np.zeros(num_ports)
sharpe_arr = np.zeros(num_ports)

for ind in range(num_ports):

    weight = np.array(np.random.random(4))

    weight = weight / np.sum(weight)

    all_weight[ind,:] = weight

    returns_arr[ind] = np.sum((log_val_returns.mean() * weight) *252)

    volumes_arr[ind] = np.sqrt(np.dot(weight.T, np.dot(log_val_returns.cov() * 252, weight)))

    sharpe_arr[ind] = returns_arr[ind]/volumes_arr[ind]

sharpe_arr.max()

sharpe_arr.argmax()

all_weight[1419,:]

max_sr_returns = returns_arr[1419]
max_sr_volumes = volumes_arr[1419]

plt.figure(figsize=(12,8))
plt.scatter(volumes_arr,returns_arr,c=sharpe_arr,cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('volatility')
plt.ylabel('returns')

plt.scatter(max_sr_volumes,max_sr_returns,c='red',s=50,edgecolors='black')

def get_returns_volume_sharperatio(weight):
    weight = np.array(weight)
    returns = np.sum(log_val_returns.mean() * weight) * 252
    volumes = np.sqrt(np.dot(weight.T, np.dot(log_val_returns.cov() * 252, weight)))
    sr = returns/volumes
    returnsurn np.array([returns,volumes,sr])

from scipy.optimize import minimize

def neg_sharpe(weight):
    return  get_returns_volume_sharperatio(weight)[2] * -1

def check_sum(weight):
    return np.sum(weight) - 1

cons = ({'type':'eq','fun': check_sum})

bounds = ((0, 1), (0, 1), (0, 1), (0, 1))

initial_guess = [0.25,0.25,0.25,0.25]

opt_results = minimize(neg_sharpe,initial_guess,method='SLSQP',bounds=bounds,constraints=cons)

opt_results

get_returns_volume_sharperatio(opt_results.x)

frontier_y = np.linspace(0,0.3,100) 

def minimize_volatility(weight):
    return  get_returns_volume_sharperatio(weight)[1] 

frontier_volatility = []

for possible_returns in frontier_y:

    cons = ({'type':'eq','fun': check_sum},
            {'type':'eq','fun': lambda w: get_returns_volume_sharperatio(w)[0] - possible_returns})
    
    result = minimize(minimize_volatility,initial_guess,method='SLSQP',bounds=bounds,constraints=cons)
    
    frontier_volatility.append(result[])

plt.figure(figsize=(12,8))
plt.scatter(volumes_arr,returns_arr,c=sharpe_arr,cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Returns')


plt.plot(frontier_volatility,frontier_y,'g--',linewidth=3)
