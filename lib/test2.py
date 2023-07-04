import numpy as np

def clustering_coefficient(adj_matrix):
    # Calculate the degree of each vertex
    degrees = np.sum(adj_matrix, axis=1)

    # Calculate the number of triangles each vertex participates in
    triangles = np.dot(adj_matrix, np.dot(adj_matrix, adj_matrix))

    # Calculate the clustering coefficient for each vertex
    clustering_coeffs = np.zeros(len(adj_matrix))
    for i in range(len(adj_matrix)):
        k = degrees[i]
        if k >= 2:
            clustering_coeffs[i] = (2 * triangles[i, i]) / (k * (k - 1))

    return clustering_coeffs.tolist()

# Example usage
adjacency_matrix = np.array([[0, 1, 1, 0],
                             [1, 0, 1, 1],
                             [1, 1, 0, 1],
                             [0, 1, 1, 0]])

coefficients = clustering_coefficient(adjacency_matrix)
print(coefficients)
