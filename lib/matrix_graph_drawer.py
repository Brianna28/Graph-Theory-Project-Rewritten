import numpy as np

def generate_random_graph(num_nodes, edge_probability):
    adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
    
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if np.random.random() < edge_probability:
                adjacency_matrix[i, j] = 1
                adjacency_matrix[j, i] = 1
    
    return adjacency_matrix

def generate_wheel_graph(num_nodes):
    adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
    
    # Connect nodes in a cycle
    for i in range(num_nodes - 1):
        adjacency_matrix[i, i+1] = 1
        adjacency_matrix[i+1, i] = 1
    
    # Connect the last node with all others
    adjacency_matrix[num_nodes-1, 0] = 1
    adjacency_matrix[0, num_nodes-1] = 1
    
    return adjacency_matrix


def generate_barabasi_albert_graph(num_nodes, num_edges_to_attach, existing_graph=None):
    if existing_graph is None:
        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        degrees = np.zeros(num_nodes, dtype=int)

        # Connect the first two nodes
        adjacency_matrix[0, 1] = 1
        adjacency_matrix[1, 0] = 1
        degrees[0] += 1
        degrees[1] += 1
    else:
        existing_size = existing_graph.shape[0]
        if num_nodes < existing_size:
            raise ValueError("Number of nodes cannot be smaller than the existing graph size.")

        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        adjacency_matrix[:existing_size, :existing_size] = existing_graph
        degrees = np.sum(adjacency_matrix, axis=0)

    # Attach the remaining nodes
    for new_node in range(existing_size, num_nodes):
        # Calculate the probability distribution based on node degrees
        probabilities = degrees[:new_node] / np.sum(degrees[:new_node])
        
        # Select nodes to attach to based on preferential attachment
        targets = np.random.choice(new_node, size=num_edges_to_attach, replace=False, p=probabilities)

        # Connect the new node to selected nodes
        adjacency_matrix[new_node, targets] = 1
        adjacency_matrix[targets, new_node] = 1

        # Update degrees of the new node and selected nodes
        degrees[new_node] += num_edges_to_attach
        degrees[targets] += 1

    return adjacency_matrix

if __name__ == '__main__':
    
    print(generate_random_graph(3,0.5))