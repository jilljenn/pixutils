import numpy as np
from sklearn.cluster import dbscan
from utils.stats import display_cluster
from leven import levenshtein


def lev_metric(data, x, y):
    i, j = int(x[0]), int(y[0])     # extract indices
    return levenshtein(data[i], data[j])


def get_clusters(results, eps=3, min_samples=5):
    data = list(results.keys())
    X = np.arange(len(data)).reshape(-1, 1)
    groups = dbscan(X, metric=lambda x, y: lev_metric(data, x, y),
                    eps=eps, min_samples=min_samples)
    core_samples, labels = groups

    clusters = {}
    for i, sample in enumerate(data):
        clusters.setdefault(labels[i], []).append(sample)
    for key in sorted(clusters):
        print('# Type', key)
        print(len(clusters[key]), 'réponses dont :')
        display_cluster(results, clusters[key], 15)
