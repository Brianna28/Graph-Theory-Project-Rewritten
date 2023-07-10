import numpy as np
from time import perf_counter


def test_average_clustering_coefficient(adjacency_matrix):
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


def average_clustering_coefficient(adjacency_matrix):
    n = adjacency_matrix.shape[0]
    clustering_coefficients = np.zeros(n)

    for i in range(n):
        neighbors = np.nonzero(adjacency_matrix[i])[0]
        k = len(neighbors)

        if k <= 1:
            clustering_coefficients[i] = 0.0
        else:
            num_edges = np.sum(adjacency_matrix[neighbors][:, neighbors]) // 2
            clustering_coefficients[i] = 2 * num_edges / (k * (k - 1))

    return float(np.mean(clustering_coefficients))


if __name__ == "__main__":
    print("h")
    # A = graph_drawer.generate_random_graph(500,0.5)
    # time = perf_counter()
    # print(average_clustering_coefficient(A))
    # print(f"org: {perf_counter()-time}")
    # time = perf_counter()
    # print(test_average_clustering_coefficient(A))
    # print(f"New: {perf_counter()-time}")
