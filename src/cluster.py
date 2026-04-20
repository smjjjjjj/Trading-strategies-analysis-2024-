import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

def cluster(timeseries, correlation_bound = 0.7):
    N = np.shape(timeseries)[0]
    T = np.shape(timeseries)[1]
    correlation_matrix = np.corrcoef(timeseries)
    
    # Convert the (historical) correlation matrix into distance matrix and extracts only its upper triangular part
    distance = 1-correlation_matrix
    condensed_dist = distance[np.triu_indices_from(distance, k=1)]
    
    # Perform agglomerative hierarchical clustering using average linkage, forming cluster.
    linkage_matrix = linkage(condensed_dist, method='average')
    clusters = fcluster(linkage_matrix, t= 1 - correlation_bound, criterion='distance')
    return clusters

def build_cluster_dict(cluster_labels, stock_names):
    cluster_dict = {}

    for i, label in enumerate(cluster_labels):
        cluster_dict.setdefault(label, []).append(stock_names[i])

    return cluster_dict