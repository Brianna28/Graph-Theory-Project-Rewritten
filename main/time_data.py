import numpy as np
from time import perf_counter
from sirdmodel import model
from lib.matrix_graph_drawer import graph_drawer
import pandas as pd
from tqdm import tqdm


def time(n):
    time = perf_counter()
    model(n,0.6,0.2)
    return perf_counter()-time

def data():
    n = {50*i:graph_drawer.generate_random_graph(50*i,0.5) for i in range(1,50)}
    results = {x:time(n.get(x)) for x in tqdm(n)} 
    done = pd.DataFrame.from_dict(results,orient='index')
    done.to_csv('data.csv')





if __name__ == '__main__':
    data()