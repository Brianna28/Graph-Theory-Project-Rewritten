from time import perf_counter
from copy import deepcopy
import numpy as np
from lib.matrix_graph_drawer import graph_drawer

def test_betterdiameter(G: np.ndarray) -> int:
    """This function calculates the diameter of a graph using matrix multiplications.

    It does this by the following fact:
    Let A be the adjacency matrix of a graph
    It can be seen that A^k where k is an integer that if the entries of A are greater then 0 it is possible to reach that node in k steps
    Thus the smallest k s.t. all the entries of A are greater than 0 k is the diameter of the graph



    Args:
        G (nx.Graph): The graph we would like to test

    Returns:
        int: The diameter of the graph
    """
    A = G.copy()
    dimensions = A.shape  # We take the dimensions of A
    # Here we add the identity matrix to A, we do this to add self loops to the graph, we do this to make sure that at odd number steps we can get back to the orginal node so the entry is not 0
    np.fill_diagonal(A, 1)
    # This is equal to A and will not change as we need this to raise A to successive powers
    const_A = A.copy()
    t = 1  # The miniumn diameter of a graph must be 1
    # if the graph is disconncetd its diamter is infinite
    #if not nx.is_connected(G) is True:
    #    return np.inf  # infinity
    for _ in range(1000):  # We interate this for 1000 trials
        # This counts how many non zeros are in the matrix
        x = np.count_nonzero(A)
        # If the number of nonzeros is equal to the size of the matrix, all values are non zero
        if x == dimensions[0]**2:
            return t  # retunr the diameter
        else:
            t += 1  # Increate t by 1
            A = A @ const_A  # raise A to 1 higher power
            # for all entries greater than 0 make them size unint8 and set them to 1. as we only care if the entry is greater than 0 and the entries will get large in size we set them to 1 to make it quicker
            A = (A > 0).astype(np.uint8)
    else:
        return np.inf


def betterdiameter(G: np.ndarray) -> int:
    """This function calculates the diameter of a graph using matrix multiplications.
    
    Args:
        A (np.ndarray): The adjacency matrix of the graph
    
    Returns:
        int: The diameter of the graph
    """
    A =  G.copy()
    np.fill_diagonal(A, 1)  # Add self-loops
    
    t = 1  # The minimum diameter of a graph is 1
    
    for _ in range(1000):
        B = np.linalg.matrix_power(A, t)  # Raise A to the power of t
        
        if np.all(B > 0):  # Check if all entries are greater than 0
            return t  # Return the diameter
        
        t += 1  # Increase t by 1
        
        A = np.logical_or(A, B)  # Element-wise logical OR of A and B
    
    return np.inf




if __name__ == '__main__':
    #K = nx.barabasi_albert_graph(10, 7)
    K = graph_drawer.generate_random_graph(10000,0)
    t = perf_counter()
    #my = betterdiameter(K)
    #print(f'My algoirthim took {perf_counter() - t},{my=}')
    t = perf_counter()
    kl = test_betterdiameter(K)
    print(f'My algoirthim took {perf_counter() - t},{kl=}')
