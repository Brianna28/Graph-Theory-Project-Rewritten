import numpy as np

def average_clustering_coefficient(adjacency_matrix):
    num_nodes = adjacency_matrix.shape[0]
    clustering_coefficients = []

    for node in range(num_nodes):
        neighbors = np.nonzero(adjacency_matrix[node])[0]
        k = len(neighbors)
        
        if k < 2:
            clustering_coefficients.append(0.0)
            continue

        num_edges = 0
        for i in range(k - 1):
            for j in range(i + 1, k):
                if adjacency_matrix[neighbors[i], neighbors[j]]:
                    num_edges += 1

        clustering_coefficient = 2.0 * num_edges / (k * (k - 1))
        clustering_coefficients.append(clustering_coefficient)

    avg_clustering_coefficient = np.mean(clustering_coefficients)
    return avg_clustering_coefficient