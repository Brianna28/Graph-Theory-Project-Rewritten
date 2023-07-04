import numpy as np

def average_shortest_path_length(adj_matrix):
    num_vertices = len(adj_matrix)
    dist = np.full(adj_matrix.shape, np.inf)
    np.fill_diagonal(dist, 0)
    dist[adj_matrix != 0] = 1

    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])

    total_distance = np.sum(dist[dist != np.inf])
    num_pairs = np.sum(dist != np.inf) - num_vertices
    average_path_length = total_distance / num_pairs

    return average_path_length