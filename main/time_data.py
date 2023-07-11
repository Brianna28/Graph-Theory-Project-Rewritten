import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)



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

def gen_graphs()->dict[int,np.ndarray[int,int]]:
    graphs = [graph_drawer.generate_random_graph(100*i,0.5) for i in range(1,25)]    
    h = [100*i for i in range(1,25)]
    done = dict(zip(h,graphs))
    return done



def data():
    done = pd.DataFrame()
    for _ in tqdm(range(5)):
        n = gen_graphs()
        results = {x:time(n.get(x)) for x in n} 
        results = pd.DataFrame.from_dict(results,orient='index')
        done = pd.concat((done,results))
    #done = pd.DataFrame.from_dict(results,orient='index')
    finished = done.sort_index()
    finished.to_csv('data.csv')





if __name__ == '__main__':
    data()