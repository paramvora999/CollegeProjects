import csv

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth

input_file = 'sales.csv'
file_read = csv.reader(open(input_file, 'r'), delimiter=',')
X = []
for cnt, row in enumerate(file_read):
    if not cnt:
        names = row[1:]
        continue

    X.append([float(x) for x in row[1:]])

# Converting to numpy array
X = np.array(X)

# Estimating the bandwidth of input data
bandwidth = estimate_bandwidth(X, quantile=0.8, n_samples=len(X))

# Clustering with MeanShift
ms_model = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms_model.fit(X)
label = ms_model.label_
cluster_center = ms_model.cluster_center_
num_cluster = len(np.unique(label))

print("\nNumber of clusters in input data =", num_cluster)

print("\nCenters of clusters:")
print('\t'.join([n[:3] for n in name]))
for cluster_c in cluster_centers:
    print('\t'.join([str(int(x)) for x in cluster_c]))

# Extracting two features for visualization 
cluster_center_2d = cluster_center[:, 1:3]

# Plotting the cluster centers 
plt.figure()
plt.scatter(cluster_center_2d[:,0], cluster_center_2d[:,1], 
        s=120, edgecolors='black', facecolors='none')

offset = 0.25
plt.xlim(cluster_center_2d[:,0].min() - offset * cluster_center_2d[:,0].ptp(),
        cluster_center_2d[:,0].max() + offset * cluster_center_2d[:,0].ptp(),)
plt.ylim(cluster_center_2d[:,1].min() - offset * cluster_center_2d[:,1].ptp(),
        cluster_center_2d[:,1].max() + offset * cluster_center_2d[:,1].ptp())

plt.title('Centers of 2D clusters')
plt.show()
