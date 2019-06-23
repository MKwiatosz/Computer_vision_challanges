# Distance 
#
# Note:
#       The R-Trees can be used, but i don't know if it's a good idea
#       Therefore DBSCAN is used as the most optimal solution for
#       clustering.
#

from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

# generate some blobs as the center of recangle

# generate some random cluster data
# X, y = make_blobs(random_state=170, n_samples=10, centers = 5)
# rng = np.random.RandomState(74)
# # transform the data to be stretched
# transformation = rng.normal(size=(2, 2))
# X = np.dot(X, transformation)

# simple defeinition of the recangle centers

X = np.array([[0,0],
                [2,2],
                [2,3],
                [4,5],
                [9,1],
                [11,3],
                [10,4],
                [12,6]])

# Plot centers of recnangle
plt.scatter(X[:, 0], X[:, 1])
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

# Max distance to other polygon 
L = 1.3


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Cluster the data into five clusters
dbscan = DBSCAN(eps=L, min_samples = 1)
clusters = dbscan.fit_predict(X_scaled)

# Plot the cluster assignments
plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap="plasma")
plt.xlabel("Y")
plt.ylabel("X")
plt.show()

# Print labels for particular polygon ( number of cluster where polygon belong)
# 
# -1 is reserved for a noise (outliners)
# 
labels = dbscan.labels_
print('Labels for particular polygon: ', labels[1:len(X)])

# Print Number of clusters
realClusterNum=len(set(labels)) - (1 if -1 in labels else 0)
clusterNum = len(set(labels))
print(realClusterNum)
print('Number of clusters: ', clusterNum)
