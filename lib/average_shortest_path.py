import numpy as np
from time import perf_counter
from scipy.sparse.csgraph import floyd_warshall

def test_average_shortest_path_length(adj_matrix: np.ndarray) -> float:
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

def tester_average_shortest_path_length(adj_matrix: np.ndarray):
    num_vertices = len(adj_matrix)
    dist = np.where(adj_matrix != 0, 1, np.inf)
    np.fill_diagonal(dist, 0)

    for k in range(num_vertices):
        dist = np.minimum(dist, np.add.outer(dist[:, k], dist[k, :]))

    total_distance = np.sum(dist[dist != np.inf])
    num_pairs = np.sum(dist != np.inf) - num_vertices
    average_path_length = total_distance / num_pairs

    return average_path_length


def average_shortest_path_length(adj_matrix: np.ndarray)-> float:
    dist_matrix = floyd_warshall(adj_matrix, directed=False, unweighted=True)
    np.fill_diagonal(dist_matrix, 0)

    total_distance = np.sum(dist_matrix)
    num_vertices = adj_matrix.shape[0]
    num_pairs = num_vertices * (num_vertices - 1)
    average_path_length = total_distance / num_pairs

    return average_path_length


if __name__ == '__main__':
    from lib.matrix_graph_drawer import graph_drawer
    print('h')
    A = graph_drawer.generate_random_graph(500,0.5)
    time = perf_counter()
    print(average_shortest_path_length(A))
    print(f"org: {perf_counter()-time}")
    time = perf_counter()
    print(tester_average_shortest_path_length(A))
    print(f"New: {perf_counter()-time}")
